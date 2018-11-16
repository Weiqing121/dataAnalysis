import matplotlib.pyplot as plt
import sys

class PlotData(object):
	def __init__(self, recipe_name, max_line):
		self.recipe_name = recipe_name
		path = "data/" + str(self.recipe_name)
		self.meal_list = {}
		self.initial_meal_list(path, max_line)
		#print(self.meal_list)

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
	def plot_meal(meal_list):
		for meal in meal_list:
			print(meal)
			x = []
			y = []
			for data in meal_list[meal]["data"]:
				x.append(data[0])
				y.append(data[1])
			plt.plot(x,y)
		plt.show()

#plot = PlotData(recipe_name = sys.argv[1], max_line = int(sys.argv[2]))
#plot = TemperaturePlot(recipe_name = sys.argv[1], max_line = 100)
#plot.PlotData(meal_list = plot.meal_list, meal_id_list = plot.meal_list.keys())