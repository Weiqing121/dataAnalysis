import numpy as np
import sys
import math

from scipy.spatial.distance import euclidean
from lib import fastdtw
from os import listdir
from os.path import isfile, join

def load_temperature_data(recipe_name, meal_id):
	temperature_list = open("data/temperatureData" + str(recipe_name) + "/" + str(meal_id)).readline()[1:][:-2].split(',')
	data_set = []
	i = 0
	for temperature in temperature_list:
		data_set.append([i,round(float(temperature),2)])
		i += 10
	return data_set

def print_result(error, max_stddev = None):
	print("id", "   error", "   std")
	values = error.values()
	mean = sum(values)/len(values)
	stddev = (sum((value - mean)**2 for value in values) / len(values))**0.5
	if max_stddev is None:
		max_key = max(error, key=error.get)
		for key in error.keys():
			if key == max_key:
				print(key, round(error[key], 2) + " --- failed")
			else:
				print(key, round(error[key], 2))
	else:
		for key in error.keys():
			error_stddev = round((error[key] - mean)/stddev, 2)
			if error_stddev >= max_stddev:
				print(key, round(error[key], 2), error_stddev, " --- failed")
			else:
				print(key, round(error[key], 2), error_stddev)

def get_meal_list(recipe_name):
	path = "data/temperatureData" + str(recipe_name) + "/"
	return [f for f in listdir(path) if isfile(join(path, f))]

def calculate_error(recipe_name, meal_list, if_print_result = True, max_stddev = None):
	i = 0
	error = {}
	for meal in meal_list:
		error[meal] = 0

	for meal_a in meal_list:
		i += 1
		for meal_b in meal_list[i:]:
			x = load_temperature_data(sys.argv[1], meal_a)
			y = load_temperature_data(sys.argv[1], meal_b)
			distance, path = fastdtw(x, y, dist=euclidean)
			#print(meal_a, meal_b, distance)
			error[meal_a] += distance
			error[meal_b] += distance

	if if_print_result:
		print_result(error, max_stddev)


calculate_error(recipe_name = sys.argv[1], meal_list = get_meal_list(sys.argv[1]), max_stddev = float(sys.argv[2]))