from population import Population
from termcolor import colored
from tqdm import tqdm
import argparse
import util
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='file input: -f example.txt')
parser.add_argument('-t', help='type input: -t ADJM or EUC2D')
args = vars(parser.parse_args())

if None in args.values() or ("ADJM" not in args.values() and "EUC2D" not in args.values()):
	print(colored("\033[1m"+"\n => Invalid Parameters! Use --help.\n", "red"))
	sys.exit()

try:

	if args['t'] == "EUC2D":
		coordinates = util.read_coordinates(args['f'])
		adj_matrix, size_indiv = util.create_adj_matrix(coordinates)
	else: 
		adj_matrix, size_indiv = util.read_adj_matrix(args['f'])

except Exception as e:
	print(colored("\033[1m"+"\n => [ERROR]: An error occurred while reading the input file, check the file and its format!\n", "red"))
	print(" => ", e, "\n")
	sys.exit()

population = Population(adj_matrix, size_indiv, nindiv=100, nger=1000, crossing_rate=0.8, mutation_rate=0.01, elitism=True)
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
		      colored("\033[1m"+"\n  => Gerations: ", "blue"), current_ger+1)
		print(colored("\033[1m"+"  => Avg fitness: ", "blue"), population.avg_fitness)
		print(colored("\033[1m"+"  => Median fitness: ", "blue"), population.median_fitness)
		print(colored("\033[1m"+"  => Std fitness: ", "blue"), population.std_fitness, end='\n\n')

print("")