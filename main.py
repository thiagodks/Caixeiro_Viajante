from concurrent.futures import ProcessPoolExecutor
from population import Population
import matplotlib.pyplot as plt
from termcolor import colored
import matplotlib.transforms
import multiprocessing
from tqdm import tqdm
import pandas as pd
import itertools
import argparse
import util
import sys
import time

def exec_ag(prmt):
	
	population = Population(adj_matrix, size_indiv, nindiv=prmt[0], nger=prmt[1], crossing_rate=prmt[2], mutation_rate=prmt[3], elitism=prmt[4])
	population.init_pop()

	for current_ger in range(0, population.nger):
		population.evaluate_pop()
		population.roulette() 
		population.ox_crossover()
		population.calculate_log()
		population.replace_pop()

	return population

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='file input: -f example.txt')
parser.add_argument('-t', help='type input: -t ADJM or EUC2D')
parser.add_argument('-p', help='parallel execution: -p 1 or 0')
parser.add_argument('-s', help='value of the best solution: -s 291')
args = vars(parser.parse_args())

if ("ADJM" not in args.values() and "EUC2D" not in args.values()) or (args['p'] != '1' and args['p'] != '0'):
	print(colored("\033[1m"+"\n => Invalid Parameters! Use --help.\n", "red"))
	sys.exit()

try:

	if args['t'] == "EUC2D":
		coordinates = util.read_coordinates(args['f'])
		adj_matrix, size_indiv = util.create_adj_matrix(coordinates)
	else: 
		adj_matrix, size_indiv = util.read_adj_matrix(args['f'])
		print(adj_matrix)

except Exception as e:
	print(colored("\033[1m"+"\n => [ERROR]: An error occurred while reading the input file, check the file and its format!\n", "red"))
	print(" => ", e, "\n")
	sys.exit()

file = args['f'].split("/")
PARALLEL_EXEC = int(args['p'])

print("\033[1m"+"\n => File: ", args['f'])
print("\033[1m"+" => Type input: ", args['t'])
print("\033[1m"+" => value of the best solution: ", args['s'], "\n")
time.sleep(2)

if not PARALLEL_EXEC:

	population = Population(adj_matrix, size_indiv, nindiv=100, nger=1000, crossing_rate=1, mutation_rate=0.01, elitism=True)
	population.init_pop()
	print("\033[1m"+population.get_parameters(), end='\n\n')

	for current_ger in tqdm(range(0, population.nger), position=0, leave=True):
		population.evaluate_pop()
		population.roulette() 
		population.ox_crossover()
		population.calculate_log()
		population.replace_pop()
		
		if (current_ger % (population.nger * 0.01)) == 0 or current_ger == population.nger-1:
			print(colored("\033[1m"+"\n\n  => Best Individual: ", "blue"), population.best_individual.fitness,
			      colored("\033[1m"+"\n  => Gerations: ", "blue"), current_ger)
			print(colored("\033[1m"+"  => Avg fitness: ", "blue"), population.avg_fitness)
			print(colored("\033[1m"+"  => Median fitness: ", "blue"), population.median_fitness)
			print(colored("\033[1m"+"  => Std fitness: ", "blue"), population.std_fitness, end='\n')

	util.plot_graphics(population, file[len(file)-1]+"_vbs:"+str(args['s'])+"_")
	answer = input("\033[1m"+" => View best solution? (y/n): ")
	if answer.lower() == "y":
		print("\n => Path ("+str(population.best_individual.fitness)+"): \n", population.best_individual.chromosome, end='\n\n')

else:
	
	npop = [50, 100, 150]
	nger = [100, 500, 1000]
	mutation_rate = [0.01, 0.05, 0.1]
	crossing_rate = [0.6, 0.8, 1]
	elitism = [True, False]

	print("\033[1m"+" => npop: ", npop)
	print("\033[1m"+" => nger: ", nger)
	print("\033[1m"+" => mutation_rate: ", mutation_rate)
	print("\033[1m"+" => crossing_rate: ", crossing_rate)
	print("\033[1m"+" => elitism: ", elitism, "\n")

	all_list = [npop, nger, crossing_rate, mutation_rate, elitism]
	parameters = list(itertools.product(*all_list)) 
	executor = ProcessPoolExecutor()
	num_args = len(parameters)
	chunksize = int(num_args/multiprocessing.cpu_count())

	results = [i for i in tqdm(executor.map(exec_ag, parameters),total=num_args)]

	best_solution = results[0]
	worst_solution = results[0]

	results_ord = []
	for i, population in enumerate(results):
		if population.best_individual.fitness < best_solution.best_individual.fitness:
			best_solution = population
		if population.best_individual.fitness == best_solution.best_individual.fitness:
			if population.nger < best_solution.nger:
				best_solution = population
		if population.best_individual.fitness > worst_solution.best_individual.fitness:
			worst_solution = population
		results_ord.append((i, population.best_individual.fitness))

	results_ord.sort(key=lambda x: x[1])
	results_ord = results_ord[:50]

	util.plot_table(results, results_ord, file)
	util.plot_graphics(best_solution, file[len(file)-1]+"_best_solution")
	util.plot_graphics(worst_solution, file[len(file)-1]+"_worst_solution")

	print(colored('\033[1m'+"\n#####################################\n-> Best solution found: ", "green"))
	print(best_solution.get_parameters())
	print(colored('\033[1m'+"\n-> Best Individual: %.10f" % best_solution.best_individual.fitness, "green")) 
	print(colored('\033[1m'+"\n-> Avg Fitness : %.10f" % best_solution.avg_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Median Fitness : %.10f" % best_solution.median_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % best_solution.std_fitness, "blue")) 

	print(colored('\033[1m'+"\n#####################################\n-> Worst solution found: ", "red")) 
	print(worst_solution.get_parameters())
	print(colored('\033[1m'+"\n-> Best Individual: %.10f" % worst_solution.best_individual.fitness, "green")) 
	print(colored('\033[1m'+"\n-> Avg Fitness : %.10f" % worst_solution.avg_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> Median Fitness : %.10f" % worst_solution.median_fitness, "blue")) 
	print(colored('\033[1m'+"\n-> STD Fitness : %.10f" % worst_solution.std_fitness, "blue")) 