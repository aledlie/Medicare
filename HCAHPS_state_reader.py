#import libraries 
import csv
import sys
#import pyodbc as p
import re
import string
import sqlite3 as sql
import itertools
from datetime import datetime 

##############################################
## connect to ESP database and open cursor  ##
##############################################

try: 
	con = sql.connect('MedicareData.db')
	cur = con.cursor()

except: 
	print "There was an error creating the database"

#initialize variables
rownum = 0
count = 0
table = []
providers = []
services = []
##############################################
##       Formatting Methods		    ##
##############################################

#method to check for date values in table
def valid_date(datestring):
	try: 
		datetime.strptime(datestring, '%m/%d/%Y')
		return True
	except ValueError:
		return False

#format date string to SQL format
def sql_date_format(datestring):
	date = datetime.strptime(datestring, '%m/%d/%Y') 
	return date.strftime('%Y-%m-%d')			

#Change 'Not Availible' to SQL Null
def NAtoNull(string):
	if str(string) == 'Not Available':
		return ''
	else:
		return string

#########################################################
## Read from .csv file into Key-Value mapping 'tables' ##
#########################################################

f = open(sys.argv[1], 'rt')
try:
	dialect = csv.excel()	
	reader = csv.reader(f, dialect)
	#read in .csv file, store in 2D array
	for row in reader:
		L = []
		#Save header row
		if rownum == 0:
			header = row
		else:
			colnum = 0	
			for col in row:
				if valid_date(str(col)):
					col = sql_date_format(str(col))
				L.append(col)
					#print '%s: %d: %s' % (header[colnum], colnum, col)	
				colnum = colnum + 1
		print "\n"
		if (len(L) > 0):
			table.append(L)
		rownum = rownum + 1
		count  = count + 1
finally:
	f.close()

print "There are %d total entries" %(count)
rows = cur.fetchall()
for row in rows:
	print row
#Alter providers table to add County and Phone Number information
#cur.execute("Select * from Providers")
#cur.execute("PRAGMA table_info(Providers)")
#print cur.fetchall()

############################################
##    CREATE HCAHPS State TABLE		  ##
############################################
cur.execute("DROP TABLE IF EXISTS StateSurveys")
cur.execute("""
CREATE TABLE StateSurveys (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	State varchar(2),
	HCAHPS_MeasureID varchar(100),
	HCAHPSAnswerPercent int,
	Footnote int,
	StartDate date,
	EndDate date
)""")

############################################
##	Add Data to Hospital Reviews	  ##
############################################
success = 0
fail = 0
for value in table:
	cur.execute("""
		INSERT INTO StateSurveys(State, HCAHPS_MeasureID, HCAHPSAnswerPercent, Footnote, StartDate, EndDate) VALUES( ?, ?, ?, ?, ?, ?)
		""", (value[0], value[2], value[4], value[5], value[6], value[7]))  
#for value in table:
#	try:
#		cur.execute("""
#			INSERT INTO HCAHPSMeasure(ID, Question, Answer) VALUES(?, ?, ?) 
#			""", (value[8], value[9], value[10]))
#		success += 1
#	except: 
#		fail += 1
#print "Out of %d attempts, there were %d successes and %d duplicates" %(success + fail, success, fail)
#con.commit()
rows = cur.execute("Select * From StateSurveys").fetchall()
for row in rows:
	print row
	

