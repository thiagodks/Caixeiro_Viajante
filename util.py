from scipy.spatial import distance
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np
import pandas as pd

def read_adj_matrix(file_name, sep=" ", type_file='EUC2D', start_line=0):

	dir_path = file_name
	size_indiv = sum(1 for _ in open(dir_path))
	adj_matrix = np.zeros((size_indiv, size_indiv), dtype=np.int32)
	file = open(dir_path, "r")
	
	for i, row in enumerate(file):
		values = row.split(sep)
		adj_matrix[i] = [int(j) for j in values if j.isdigit()]

	return adj_matrix, size_indiv

def read_coordinates(file_name, sep=" ", start_line=6):
	dir_path = file_name
	size_indiv = sum(1 for _ in open(dir_path)) - start_line
	file = open(dir_path, "r")
	coordinates = []
	for i, row in enumerate(file):
		if i >= start_line: 
			values = row.split(sep)
			values = [x for x in values if x != '']
			coordinates.append((float(values[1]), float(values[2].replace("\n", ""))))

	if len(values) != 3: raise Exception('Input file incompatible with the type provided') 
	return coordinates

def create_adj_matrix(coordinates):
	num_cities = len(coordinates)
	adj_matrix = np.zeros((num_cities, num_cities), dtype=np.int32)
	for i in range(0, num_cities):
		for j in range(0, num_cities):
			dist = int(distance.euclidean(coordinates[i], coordinates[j]) + 0.5)
			adj_matrix[i][j] = dist
			
	return adj_matrix, num_cities

def plot_graphics(population, name_save=""):

	log_ger = list(map(list, zip(*population.log_ger)))
	best_ger, avg_ger, median_ger, std_fitness = log_ger[0], log_ger[1], log_ger[2], log_ger[3]

	fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
	fig.set_size_inches(30, 9)
	title = fig.suptitle('Fitness - AG', fontsize=40, x=0.45, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.04, right=0.85, top=0.85)
	plt.gcf().text(0.86, 0.25, (population.get_parameters() + 
					 '\n\n-----------------------------------------\n\n Melhor Fitness: ' + str (population.best_individual.fitness) +
					 '\n\n Media Fitness: %.2f' % population.avg_fitness +
					 '\n\n Mediana Fitness: %.2f' % population.median_fitness +
					 '\n\n Std Fitness: %.2f' % population.std_fitness), fontsize=16)

	if population.nger >= 100: step = int(population.nger / 100)
	else: step = 1
	avg_ger_step, median_ger_step, best_ger_step = [], [], []
	for i in range(0, population.nger, step):
		avg_ger_step.append(avg_ger[i])
		median_ger_step.append(median_ger[i])
		best_ger_step.append(best_ger[i])

	ax1.set_title("Melhores fitness a cada geração (1 a "+str(population.nger)+")")
	ax1.set_xlabel("Gerações", fontsize='medium')
	ax1.set_ylabel("Fitness", fontsize='medium')
	ax1.plot(list(range(0, population.nger, step)), best_ger_step, 'g--', label='Melhor Fitness: ' + str (population.best_individual.fitness))
	ax1.legend(ncol=3)
	ax1.tick_params(labelsize=18)

	ax2.set_title("Media e Mediana da fitness a cada geração")
	ax2.set_xlabel("Gerações", fontsize='medium')
	ax2.set_ylabel("Fitness", fontsize='medium')

	ax2.plot(list(range(0, population.nger, step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % population.avg_fitness)
	ax2.plot(list(range(0, population.nger, step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % population.median_fitness)
	ax2.legend(ncol=1)
	ax2.tick_params(labelsize=18)

	ax3.set_title("Comparação entre as fitness a cada geração")
	ax3.set_xlabel("Gerações", fontsize='medium')
	ax3.set_ylabel("Fitness", fontsize='medium')
	ax3.plot(list(range(0, population.nger, step)), best_ger_step, 'g--', label='Melhor Fitness: %.4f' % population.best_individual.fitness)
	ax3.plot(list(range(0, population.nger, step)), avg_ger_step, 'r--', label='Media Fitness: %.4f' % population.avg_fitness)
	ax3.plot(list(range(0, population.nger, step)), median_ger_step, 'b--', label='Mediana Fitness: %.4f' % population.median_fitness)
	ax3.legend(ncol=1)
	ax3.tick_params(labelsize=18)

	print(colored("\033[1m"+"\n => Graphic saved in: " + 'graficos/'+name_save+population.file_name+'fitness.png', "green"))
	fig.savefig('graficos/'+name_save+population.file_name+'fitness.png')

def plot_table(results, results_ord):
	table = {"NPOP": [], "NGER": [], "TX_M": [], "TX_C": [], "Elitism": [],
			 "Fitness": [], "Avg Fit": [], "Median Fit": [], "STD": []}
	
	for i in results_ord:
		table["NPOP"].append(results[i[0]].nindiv)
		table["NGER"].append(results[i[0]].nger)
		table["TX_M"].append(results[i[0]].mutation_rate)
		table["TX_C"].append(results[i[0]].crossing_rate)
		table["Elitism"].append(results[i[0]].elitism)
		table["Fitness"].append(results[i[0]].best_individual.fitness)
		table["Avg Fit"].append("%.2f" % results[i[0]].avg_fitness)
		table["Median Fit"].append("%.2f" % results[i[0]].median_fitness)
		table["STD"].append("%.2f" % results[i[0]].std_fitness)

	df = pd.DataFrame(data=table)
	print("\nTable results: \n", df)

	fig, ax = plt.subplots()

	fig.patch.set_visible(False)
	plt.axis('off')
	plt.grid('off')
	fig.set_size_inches(12, 11)

	the_table = ax.table(cellText=df.values,colLabels=df.columns, cellLoc='center', loc='center')
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(12)

	plt.gcf().canvas.draw()
	points = the_table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
	points[0,:] -= 120; points[1,:] += 120
	nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)

	fig.tight_layout()
	print(colored("\033[1m"+"\n => Table saved in: " + 'tabelas/'++file[len(file)-1]+'.png', "green"))
	fig.savefig('tabelas/'+file[len(file)-1]+'.png', dpi=500, bbox_inches=nbbox)