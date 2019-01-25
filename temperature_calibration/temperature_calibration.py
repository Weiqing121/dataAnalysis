from os import listdir
from os.path import isfile, join
from datetime import datetime
from dateutil import parser
import numpy as np

ADC_VALUE_FACTOR = 0.01

class TemperatureCalibration(object):
	def __init__(self, machine_id):
		self.path = "data/" + str(machine_id)
		self.adc_readings = {"read at": [], "data":[], "temperature":[]}
		self.temperature_measurements = {"measure at": [], "data":[]}

	def load_adc_readings(self):
		with open(self.path + "_adc.txt") as file:
			i = 0
			for line in file:
				line = line[:-1]
				i += 1
				if i == 1:
					start_at = parser.parse(line).timestamp() - 18000.0
				else:
					reading = line.split(' ')
					read_at = float(reading[0]) + start_at
					read_value = float(reading[1]) * ADC_VALUE_FACTOR
					self.adc_readings["read at"].append(read_at)
					self.adc_readings["data"].append(read_value)

	def load_temperature_measurements(self):
		with open(self.path + "_temperature.txt") as file:
			i = 0
			for line in file:
				i += 1
				if i == 1:
					continue
				if len(line) < 2:
					continue
				line = line[:-1].split(',')
				time = line[1].replace('"', '') + " " +line[2].replace('"', '')
				read_at = parser.parse(str(time)).timestamp()
				read_value = float(line[3].replace('"', ''))
				self.temperature_measurements["measure at"].append(read_at)
				self.temperature_measurements["data"].append(read_value)

	def find_range(self, time):
		if time < self.temperature_measurements["measure at"][0]:
			return None
		for i in range(len(self.temperature_measurements["measure at"]) - 1):
			if time > self.temperature_measurements["measure at"][i] and time < self.temperature_measurements["measure at"][i+1]:
				return i

	def get_temperature(self, time):
		index = self.find_range(time)
		time_range = [self.temperature_measurements["measure at"][index], self.temperature_measurements["measure at"][index+1]]
		temperature_range = [self.temperature_measurements["data"][index], self.temperature_measurements["data"][index+1]]

		return temperature_range[0] + (temperature_range[1] - temperature_range[0]) * (time - time_range[0])/(time_range[1] - time_range[0])

	def convert_to_celsius(self, data_array):
		data_in_Celsius = []
		for data_in_Fahrenheit in data_array:
			data_in_Celsius.append((data_in_Fahrenheit - 32.0) * 5.0 / 9.0)
		return data_in_Celsius

	def fitting(self):
		for i in range(len(self.adc_readings["read at"])):
			self.adc_readings["temperature"].append(self.get_temperature(self.adc_readings["read at"][i]))

		y = self.convert_to_celsius(self.adc_readings["temperature"])
		x = self.adc_readings["data"]

		return np.polynomial.polynomial.polyfit(x, y, 3)


temp_cal = TemperatureCalibration("1008-4718-1007")
temp_cal.load_adc_readings()
temp_cal.load_temperature_measurements()
print(temp_cal.fitting())

#print(temp_cal.adc_readings["temperature"])
#print(temp_cal.convert_to_celsius(temp_cal.adc_readings["temperature"]))
#print(temp_cal.adc_readings["read at"])
#print(temp_cal.temperature_measurements["measure at"])

