import random

class Individual:

	def __init__(self, size):
		self.size = size
		self.chromosome = []

	def init_chromosome(self):
		available_index = [j for j in range(0, self.size)]
		for _ in range(0, self.size):
			gene = random.choice(available_index)
			self.chromosome.append(gene)
			available_index.remove(gene)

	def mutation(self):
		pass


class Population:

	def __init__(self, adj_matrix, size_indiv, nindiv, nger):
		self.adj_matrix = adj_matrix
		self.nindiv = nindiv
		self.nger = nger
		self.size_indiv = size_indiv

	def init_pop(self):
		self.individuals = []
		
		for _ in range(0, self.nindiv):
			individual = Individual(self.size_indiv)
			individual.init_chromosome()
			self.individuals.append(individual)

		self.show_pop()

	def calc_fitness(self):
		pass

	def show_pop(self):
		print("\nPopulation ("+str(self.nindiv)+" indiv): ")
		for i in self.individuals:
			print(i.chromosome)
		input("")
