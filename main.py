import numpy as np
from population import Population

def load_file(file_name, sep=" "):

	dir_path = "instancias/"+file_name
	size_indiv = sum(1 for _ in open(dir_path))
	adj_matrix = np.zeros((size_indiv, size_indiv), dtype=np.int32)
	file = open(dir_path, "r")
	
	for i, row in enumerate(file):
		values = row.split(sep)
		adj_matrix[i] = [int(j) for j in values if j.isdigit()]

	return adj_matrix, size_indiv

adj_matrix, size_indiv = load_file("lau15_dist.txt")
population = Population(adj_matrix, size_indiv, 10, 10)
population.init_pop()