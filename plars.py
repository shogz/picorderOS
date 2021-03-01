print("Loading Picorder Library Access and Retrieval System Module")
from objects import *

#	PLARS (Picorder Library Access and Retrieval System) aims to provide a
#	single surface for retrieving data for display in any of the different
#	Picorder screen modes.



#	TO DO:
#	pull from saved data
#		All data of a certain sensor
#		All data of a certain time scale
#			Data at set intervals (last day, last hour, last minute)
# 	Incorporate short term memory

import os
import numpy
import datetime
from array import *
import pandas as pd





# Create a class that acts as the surface for all interactions with the data core
class PLARS(object):

	def __init__(self):

		# PLARS opens a data frame at initialization.
		# If the csv file exists it opens it, otherwise creates it.
		# self.df is the dataframe for the class

		self.file_path = "data/datacore.csv"

		if os.path.exists(self.file_path):
			self.df = pd.read_csv(self.file_path)
		else:
			if not os.path.exists("data"):
				os.mkdir("data")
			self.df = pd.DataFrame(columns=['value','min','max','dsc','sym','dev','timestamp'])
			self.df.to_csv(self.file_path)

		# Set floating point display to raw, instead of exponent
		pd.set_option('display.float_format', '{:.7f}'.format)

	# provide status of database (how many entries, how many devices, size, length)
	def status(self):
		pass

	# gets the latest CSV file
	def get_core(self):
		self.df = pd.read_csv(self.file_path)

	#pends a new set of data to the CSV file.
	def append_to_core(self, data):
		 data.to_csv(self.file_path, mode='a', header=False)

	# updates the data storage file with the most recent sensor fragments
	def update(self,data):
		newdata = pd.DataFrame(data,columns=['value','min','max','dsc','sym','dev','timestamp'])
		print(newdata)
		self.append_to_core(newdata)

	# returns all sensor data in the core for the specific sensor (dsc,dev)
	def get_sensor(self,dsc,dev):
		self.get_core()
		result = self.df.loc[self.df['dsc'] == dsc]
		result2 = result.loc[self.df['dev'] == dev]
		return result2

	def index_by_time(self):
		self.df.sort_values(by=['timestamp'])

	# return a list of n most recent data from specific sensor defined by key
	# seperated by a comma

	# update the buffer from disk
	# organize it by time.
	# get only n number of sensor data required
	# trim it to length.
	# return only the sensor values in a list.
	def get_recent(self, dsc, dev, num = 5):
		self.get_core()
		self.index_by_time()
		untrimmed_data = self.get_sensor(dsc,dev)
		trimmed_data = untrimmed_data.tail(num)
		return trimmed_data['value'].tolist()



	# return a number of data from a specific sensor at a specific time interval
	def get_timed(self, key, interval = 0, num = 5):
		#load csv file as dataframe
		pass

	# returns the entire datacore
	def emrg(self):
		self.get_core()
		return self.df

	def convert_epoch(self, time):
		return datetime.datetime.fromtimestamp(time)