from scipy.spatial import distance
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