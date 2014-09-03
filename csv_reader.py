import csv
import sys

f = open(sys.argv[1], 'rt')
rownum = 0
try:
	reader = csv.reader(f)
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

