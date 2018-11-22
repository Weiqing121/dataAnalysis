import numpy as np
import sys
import math

from scipy.spatial.distance import euclidean
from lib import fastdtw
from os import listdir
from os.path import isfile, join

class BinaryClassifier(object):
	def __init__(self, recipe_name):
		self.recipe_name = recipe_name
		path = "data/temperatureData" + str(self.recipe_name) + "/"
		meal_id_list = [f for f in listdir(path) if isfile(join(path, f))]

		self.failed_meal_list = {}
		self.meal_list = {}
		self.initial_meal_list(meal_id_list)

	def initial_meal_list(self, meal_id_list):
		for meal_id in meal_id_list:
			self.meal_list[meal_id] = {}
			self.meal_list[meal_id]["error"] = 0
			self.meal_list[meal_id]["stddev"] = 0
			self.meal_list[meal_id]["is_cooked"] = None

	def zero_results_in_meal_list(self):
		for meal_id in self.meal_list:
			self.meal_list[meal_id]["error"] = 0
			self.meal_list[meal_id]["stddev"] = 0

	def load_temperature_data(self, meal_id):
		temperature_list = open("data/temperatureData" + str(self.recipe_name) + "/" + str(meal_id)).readline()[1:][:-2].split(',')
		data_set = []
		i = 0
		for temperature in temperature_list:
			data_set.append([i,round(float(temperature),2)])
			i += 10
		return data_set

	def print_result(self, decimal_place = 2):
		print("id", "\terror", "\tstd")
		for meal_id in self.meal_list:
			print(self.meal_list[meal_id]["error"])
			#print(meal_id, round(self.meal_list[meal_id]["error"] / (len(self.meal_list) - 1), decimal_place), round(self.meal_list[meal_id]["stddev"], decimal_place))
		
		print("******** failed ********")
		for meal_id in self.failed_meal_list:
			#print(meal_id, '\t', round(self.failed_meal_list[meal_id]["error"] / len(self.meal_list), decimal_place), '\t', round(self.failed_meal_list[meal_id]["stddev"], decimal_place))
			print(self.failed_meal_list[meal_id]["error"])
	
	def print_meal_list(self):
		print(self.meal_list.keys())

	def print_failed_meal_list(self):
		print(self.failed_meal_list.keys())

	def get_max_error(self):
		pass

	def identify_outlier(self, max_stddev):
		# minimun one in the reference pool
		if len(self.meal_list) <= 2:
			return
			
		sum_error = 0
		is_outlier_find = False
		sum_error = sum(self.meal_list[meal_id]["error"] for meal_id in self.meal_list)
		mean = sum_error/len(self.meal_list)
		stddev = (sum((self.meal_list[meal_id]["error"] - mean)**2 for meal_id in self.meal_list) / len(self.meal_list))**0.5
		
		for meal_id in self.failed_meal_list:
			self.failed_meal_list[meal_id]["stddev"] = (self.failed_meal_list[meal_id]["error"]- mean)/stddev

		meal_id_list = list(self.meal_list.keys())
		for meal_id in meal_id_list:
			self.meal_list[meal_id]["stddev"] = (self.meal_list[meal_id]["error"]- mean)/stddev
			if abs(self.meal_list[meal_id]["stddev"]) >= max_stddev:			
				self.failed_meal_list[meal_id] = self.meal_list.pop(meal_id)
				self.failed_meal_list[meal_id]["is_cooked"] = True
				is_outlier_find = True
			else:
				self.meal_list[meal_id]["is_cooked"] = True

		if is_outlier_find:
			self.calculate_error(max_stddev)

	def calculate_error(self, max_stddev = None):
		self.zero_results_in_meal_list()

		i = 0
		meal_id_list = list(self.meal_list.keys())
		for meal_a in meal_id_list:
			i += 1
			for meal_b in meal_id_list[i:]:
				x = self.load_temperature_data(meal_a)
				y = self.load_temperature_data(meal_b)
				distance, path = fastdtw(x, y, dist=euclidean)
				self.meal_list[meal_a]["error"] += distance
				self.meal_list[meal_b]["error"] += distance

		if max_stddev is not None:
			self.identify_outlier(max_stddev)

classifier = BinaryClassifier(recipe_name = sys.argv[1])
classifier.calculate_error(max_stddev = float(sys.argv[2]))
classifier.print_meal_list()
classifier.print_failed_meal_list()