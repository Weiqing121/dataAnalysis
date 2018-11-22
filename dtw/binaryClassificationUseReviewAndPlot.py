import numpy as np
import sys
import math

from scipy.spatial.distance import euclidean
from lib import fastdtw
from os import listdir
from os.path import isfile, join
from plotData import PlotData

class ReviewClassifier(object):
	def __init__(self, recipe_name, max_line):
		self.recipe_name = recipe_name
		path = "data/temperatureData/" + str(self.recipe_name)
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
	
	def list_failed_meal_id(self, reviews_file):
		with open(reviews_file) as file:
			i = 0
			for line in file:
				print(line)

	def generate_failed_list_use_review(self, reviews_file):
		failed_meal_id_list = self.list_failed_meal_id(reviews_file)
		print(failed_meal_id_list)


classifier = ReviewClassifier(recipe_name = sys.argv[1], max_line = int(sys.argv[2]))
classifier.generate_failed_list_use_review(reviews_file = "data/reviews.csv")
#PlotData.plot_meal(meal_list = classifier.meal_list, failed_meal_list = classifier.failed_meal_list)
