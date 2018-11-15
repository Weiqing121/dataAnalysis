import csv
import sys
import os

with open(sys.argv[1]) as csvfile:
	rows = csv.DictReader(csvfile)
	# meal_id, name, root_recipe_id, version, status, created_at, est_cook_time, data 
	i = 0
	for row in rows:
		recipe_name = row["name"].split(":")[0].replace(" ","")
		file = open("data/" + recipe_name, "a+")
		file.write(row["meal_id"] + " " + row["data"] + "\n")
		file.close()
