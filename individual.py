import random
import numpy as np

class Individual:

	def __init__(self, size, mutation_rate):
		self.size = size
		self.mutation_rate = mutation_rate
		self.chromosome = []
		self.fitness = None

	def init_chromosome(self):
		available_index = [j for j in range(0, self.size)]
		for _ in range(0, self.size):
			gene = random.choice(available_index)
			self.chromosome.append(gene)
			available_index.remove(gene)

	def obj_funct(self, adj_matrix):
		distance = 0
		for i in range(0, len(self.chromosome)-1):
			distance += adj_matrix[self.chromosome[i]][self.chromosome[i+1]]
		distance += adj_matrix[self.chromosome[i+1]][self.chromosome[0]]
		return distance

	def calc_fitness(self, adj_matrix):
		self.fitness = self.obj_funct(adj_matrix)

	def mutation(self):
		for i, gene in enumerate(self.chromosome):
			if random.random() <= self.mutation_rate:
				swap_index = np.random.randint(0, self.size)
				while swap_index == i: 
					swap_index = np.random.randint(0, self.size)
				aux = self.chromosome[swap_index]
				self.chromosome[swap_index] = self.chromosome[i]
				self.chromosome[i] = aux