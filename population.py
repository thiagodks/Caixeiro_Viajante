import random
import numpy as np
from individual import Individual

class Population:

	def __init__(self, adj_matrix, size_indiv, nindiv, nger, crossing_rate, mutation_rate, elitism):
		self.adj_matrix = adj_matrix
		self.nindiv = nindiv
		self.nger = nger
		self.size_indiv = size_indiv
		self.crossing_rate = crossing_rate
		self.mutation_rate = mutation_rate
		self.elitism = elitism
		self.log_ger = []

	def init_pop(self):
		self.individuals = []
		
		for _ in range(0, self.nindiv):
			individual = Individual(self.size_indiv, self.mutation_rate)
			individual.init_chromosome()
			self.individuals.append(individual)

	def evaluate_pop(self):
		for i in range(0, len(self.individuals)):
			self.individuals[i].calc_fitness(self.adj_matrix)

	def show_pop(self, individuals, title):
		print(title, len(individuals))
		for i in individuals:
			print(i.chromosome, "fitness: " + str(i.fitness))
		input("")

	def create_indiv(self, father1, father2, point1, point2):
		individual = Individual(self.size_indiv, self.mutation_rate)
		individual.chromosome = father2.chromosome[point1:point2]
		remaining_genes = (father1.chromosome[point2:] + father1.chromosome[:point2])
		index = 0
		for gene in remaining_genes:
			if (gene not in individual.chromosome) and point2 < self.size_indiv: 
				individual.chromosome.append(gene)
				point2 += 1
			elif (gene not in individual.chromosome): 
				individual.chromosome.insert(index, gene)
				index += 1
		return individual

	def get_points(self):
		point1 = random.randint(1,(self.size_indiv) - 2)
		point2 = random.randint(1,(self.size_indiv) - 2)
		while point1 == point2: 
			point2 = random.randint(1,(self.size_indiv) - 2)
		
		if point1 < point2: return point1, point2
		return point2, point1


	def ox_crossover(self):
		self.intermediate_indiv = []
		for i in range(0, len(self.parents), 2):

			if random.random() < self.crossing_rate:

				point1, point2 = self.get_points()
				
				son1 = self.create_indiv(self.parents[i], self.parents[i+1], point1, point2)
				son2 = self.create_indiv(self.parents[i+1], self.parents[i], point1, point2)

				son1.mutation()
				son2.mutation()

				self.intermediate_indiv.append(son1)
				self.intermediate_indiv.append(son2)

	def calculate_log(self):
		self.best_individual = self.individuals[0]
		indiv_fitness = []

		for individual in self.individuals:
			if individual.fitness < self.best_individual.fitness:
				self.best_individual = individual
			indiv_fitness.append(individual.fitness)

		self.avg_fitness = np.mean(indiv_fitness)
		self.median_fitness = np.median(indiv_fitness)
		self.std_fitness = np.std(indiv_fitness)
		self.log_ger.append((self.best_individual.fitness, self.avg_fitness, self.median_fitness, self.std_fitness))


	def run_elitism(self):
		self.individuals[np.random.randint(0, self.nindiv)] = self.best_individual 

	def replace_pop(self):
		available_index = [i for i in range(0, self.nindiv)]
		num_indiv = len(self.intermediate_indiv)
		for new_indv in range(0, num_indiv):
			index = random.choice(available_index)
			self.individuals[index] = self.intermediate_indiv[new_indv]
			available_index.remove(index)

		if self.elitism: self.run_elitism()
				
	def roulette(self):
		num_parents, total_fitness = 1, 0
		self.parents, individual_fitness = [], []

		for i in range(0, len(self.individuals)):
			individual_fitness.append(1/self.individuals[i].fitness)
			total_fitness += individual_fitness[i]

		roulette_fitness = [individual_fitness[i]/total_fitness for i in range(0, len(self.individuals))]
		while num_parents <= self.nindiv:
			r = random.random()
			aux_sum = 0
			for j, value in enumerate(roulette_fitness):
				aux_sum += value
				if aux_sum >= r:
					self.parents.append(self.individuals[j])
					break
			num_parents += 1

	def get_parameters(self):
		return ("\n Elitism: " + str(self.elitism) +
		"\n Number of Individuals: " + str(self.nindiv) +
		"\n Number of Generations: " + str(self.nger) +
		"\n Number of Cities: " + str(self.size_indiv) +
		"\n Mutation Rate: " + str(self.mutation_rate) +
		"\n Crossover Rate : " + str(self.crossing_rate))
