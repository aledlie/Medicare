#import libraries 
import csv
import sys

#initialize variables
rownum = 0
FILTER_COLUMNS = ('ClientName', 'ProjectName')


f = open(sys.argv[1], 'rt')
try:
	dialect = csv.excel()	
	reader = csv.reader(f, dialect)
	for row in reader:
		#Save header row
		if rownum == 0:
			header = row
		else:
			colnum = 0
			for col in row:
				print '%-8s: %s' % (header[colnum], col)
				colnum += 1
		rownum += 1
finally:
	f.close()

