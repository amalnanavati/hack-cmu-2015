from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import csv
import os
import string

class Data(object):
	def __init__(self, keyword):
		self.word = keyword

	def getData(self):
		self.generateCSV()
		with open("data.csv", 'rb') as csvfile:
			readFile = csv.reader(csvfile, dialect='excel', quotechar='|')
			listOfValues = [ ]
			readInput = ""
			for row in readFile:
				readInput = readInput + ', '.join(row) + "\n"
			print readInput
			i = 0
			arr = readInput.splitlines()
			for line in arr:
				if (line == "Subregion, %s" % self.word.lower()):
					seenNextLine = False
					for k in xrange(1, 55):
						if (arr[i+k] == "Top metros for %s" % self.word.lower()):
							seenNextLine = True
						if (seenNextLine == False):
							stateHits = string.split(arr[i+k], ", ")
							print stateHits
							if (len(stateHits) == 2):
								listOfValues += [[stateHits[0], int(stateHits[1])]]
				i = i+1
			
		stateNameToID = {'Mississippi': 'MS', 'Northern Mariana Islands': 'MP', 'Oklahoma': 'OK', 'Wyoming': 'WY', 'Minnesota': 'MN', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Texas': 'TX', 'Tennessee': 'TN', 'Iowa': 'IA', 'Wisconsin': 'WI', 'Arizona': 'AZ', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'District of Columbia': 'DC', 'New Hampshire': 'NH', 'Idaho': 'ID', 'West Virginia': 'WV', 'South Carolina': 'SC', 'California': 'CA', 'Massachusetts': 'MA', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Florida': 'FL', 'Hawaii': 'HI', 'Kentucky': 'KY', 'Rhode Island': 'RI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 'Illinois': 'IL', 'Virgin Islands': 'VI', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'National': 'NA', 'Washington': 'WA', 'North Carolina': 'NC', 'Maine': 'ME', 'New York': 'NY', 'Montana': 'MT', 'Nevada': 'NV', 'Delaware': 'DE', 'Guam': 'GU'}
		print listOfValues
		for a in xrange(len(listOfValues)):
			listOfValues[a][0] = stateNameToID[listOfValues[a][0]]

		return listOfValues

	def generateCSV(self):
		google_username = "hackcmu2015"
		google_password = "hack2015"
		path = os.getcwd()+"/"

		# connect to Google
		connector = pyGTrends(google_username, google_password)

		# make request
		connector.request_report("%s" % self.word, hl='en-US', cat=None, geo='US', date="today 7-d")

		# wait a random amount of time between requests to avoid bot detection
		time.sleep(randint(5, 10))

		# download file
		connector.save_csv(path, "data")


# dataex = Data("pizza")
# print dataex.getData()
