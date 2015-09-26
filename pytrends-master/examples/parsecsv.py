import csv
import string

class Data(object):
	def __init__(self, filename, keyword):
		self.name = filename
		self.word = keyword

	def getData(self):
		with open(self.name, 'rb') as csvfile:
			readFile = csv.reader(csvfile, dialect='excel', quotechar='|')
			listOfValues = [ ]
			readInput = ""
			for row in readFile:
				readInput = readInput + ', '.join(row) + "\n"
			i = 0
			arr = readInput.splitlines()
			for line in arr:
				if (line == "Subregion, %s" % self.word):
					seenNextLine = False
					for k in xrange(1, 100):
						if (arr[i+k] == "Top metros for %s" % self.word):
							seenNextLine = True
						if (seenNextLine == False):
							stateHits = string.split(arr[i+k], ", ")
							if (len(stateHits) == 1):
								listOfValues += [stateHits[0]]
							else:
								listOfValues += [(stateHits[0], stateHits[1])]
				i = i+1
			
			#can uncomment if you want to print 
			# out values of list
			#for x in xrange(0, len(listOfValues)):
			#print listOfValues[x], "\n"
		return listOfValues

dataex = Data("examplespizza.csv", "pizza")
dataex.getData()
