import matplotlib.pyplot as plot

class TemperaturePlot(object):
	def __init__(self, recipe_name, max_num_data):
		self.recipe_name = recipe_name
		path = "data/" + str(self.recipe_name)

		self.failed_meal_list = {}
		self.meal_list = {}
		self.initial_meal_list(path, max_num_data)
		with open(path) as file:
			i = 0
			for line in file:
				if len(self.meal_list) > max_num_data:
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