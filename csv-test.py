import csv

with open('/Users/alyshialedlie/Downloads/CompleteProjectIndex.csv', 'r') as myfile:
	reader = csv.reader(myfile, delimiter = ' ', quotechar = '|')
	for row in reader:
		print ', '.join(row) 
