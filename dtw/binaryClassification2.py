import numpy as np
import sys
import math

from scipy.spatial.distance import euclidean
from lib import fastdtw
from os import listdir
from os.path import isfile, join
from plotData import PlotData

class BinaryClassifier(object):
	def __init__(self, recipe_name, max_line):
		self.recipe_name = recipe_name
		path = "data/" + str(self.recipe_name)
		#meal_id_list = [f for f in listdir(path) if isfile(join(path, f))]
		#meal_id_list = self.initial_meal_id_list(path)

		self.failed_meal_list = {}
		self.meal_list = {}
		self.initial_meal_list(path, max_line)

	def initial_meal_list(self, path, max_line):
		with open(path) as file:
			i = 0
			for line in file:
				if len(self.meal_list) > max_line:
					break
				meal_id = line.split()[0]
				line = line.strip(meal_id)
				line = line.strip(" {")
				line = line.strip("}\n")
				self.meal_list[meal_id] = {}
				self.meal_list[meal_id]["data"] = []
				i = 0
				for temperature in line.split(','):
					self.meal_list[meal_id]["data"].append([i,round(float(temperature),2)])
					i += 10

				self.meal_list[meal_id]["error"] = 0
				self.meal_list[meal_id]["stddev"] = 0
				self.meal_list[meal_id]["is_cooked"] = None

	def zero_results_in_meal_list(self):
		for meal_id in self.meal_list:
			self.meal_list[meal_id]["error"] = 0
			self.meal_list[meal_id]["stddev"] = 0

	def load_temperature_data(self, meal_id):
		temperature_list = open("data/" + str(self.recipe_name) + "/" + str(meal_id)).readline()[1:][:-2].split(',')
		data_set = []
		i = 0
		for temperature in temperature_list:
			data_set.append([i,round(float(temperature),2)])
			i += 10
		return data_set

	def print_result(self, decimal_place = 2):	
		print("------- cooked --------\n", "id", "\t  error", "\t std")
		for meal_id in self.meal_list:
			print(meal_id, '\t', self.meal_list[meal_id]["error"], '\t', round(self.meal_list[meal_id]["stddev"], decimal_place))
		
		print("------- failed --------")
		for meal_id in self.failed_meal_list:
			print(meal_id, '\t', self.failed_meal_list[meal_id]["error"] , '\t', round(self.failed_meal_list[meal_id]["stddev"], decimal_place))

	def print_meal_list(self):
		print(self.meal_list.keys())

	def print_failed_meal_list(self):
		print(self.failed_meal_list.keys())

	def get_max_error(self):
		pass

	def identify_outlier(self, max_stddev):
		print("..... identify_outlier .....")
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
				print(" outlier ", meal_id, self.failed_meal_list[meal_id]["error"], self.failed_meal_list[meal_id]["stddev"])
			else:
				self.meal_list[meal_id]["is_cooked"] = True
				print("... ", meal_id, self.meal_list[meal_id]["error"], self.meal_list[meal_id]["stddev"] )

		if is_outlier_find:
			self.calculate_error(max_stddev)

	def calculate_error(self, max_stddev = None):
		print("..... calculate_error .....")
		self.zero_results_in_meal_list()

		i = 0
		meal_id_list = list(self.meal_list.keys())
		for meal_a in meal_id_list:
			i += 1
			for meal_b in meal_id_list[i:]:
				x = self.meal_list[meal_a]["data"]
				y = self.meal_list[meal_b]["data"]
				distance, path = fastdtw(x, y, dist=euclidean)
				self.meal_list[meal_a]["error"] += distance
				self.meal_list[meal_b]["error"] += distance
			self.meal_list[meal_a]["error"] = round(self.meal_list[meal_a]["error"] / (len(self.meal_list) - 1), 2)
			print("...", meal_a, self.meal_list[meal_a]["error"])

		if max_stddev is not None:
			self.identify_outlier(max_stddev)
		
classifier = BinaryClassifier(recipe_name = sys.argv[1], max_line = int(sys.argv[2]))
classifier.calculate_error(max_stddev = float(sys.argv[3]))
classifier.print_result()
#classifier.print_meal_list()
#classifier.print_failed_meal_list()
PlotData.plot_meal(meal_list = classifier.meal_list)
