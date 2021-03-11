from scipy.spatial import distance
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np

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
	title = fig.suptitle('Fitness - AG', fontsize=40, x=0.52, y=0.97)

	plt.rcParams.update({'font.size': 20})
	plt.subplots_adjust(left=0.04, right=0.85, top=0.85)
	plt.gcf().text(0.86, 0.25, (population.get_parameters() + 
					 '\n\n-----------------------------------------\n\n Melhor Fitness: ' + str (population.best_individual.fitness) +
					 '\n\n Media Fitness: '+ str (population.avg_fitness) +
					 '\n\n Mediana Fitness: '+ str (population.median_fitness)+
					 '\n\n Std Fitness: %.7f' % population.std_fitness), fontsize=16)

	step = int(population.nger / 100)
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

	print(colored("\033[1m"+"\n => Graphic saved in: " + 'graficos/'+population.file_name+'fitness.png', "green"))
	fig.savefig('graficos/'+population.file_name+'fitness.png')
