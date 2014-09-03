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
				if colnum in (11, 12, 13):
					col = NAtoNull(col)
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

#update provider information table with new information
success = 0
fail = 0
for value in table:
	cur.execute("UPDATE Providers SET County = ? WHERE ID = ?", (value[6], value[0]))
	cur.execute("UPDATE Providers SET PhoneNumber = ? WHERE ID = ?", (value[7], value[0])) 
	success += 1
print "Out of %d providers were updated" %(success)


#########################################
##      Create Reviews Table	       ##
#########################################
cur.execute("DROP TABLE IF EXISTS HCAHPSMeasure")
cur.execute("DROP TABLE IF EXISTS hospital_reviews")
cur.execute("""
	CREATE TABLE HCAHPSMeasure(
		ID varchar(100) PRIMARY KEY,
		Question varchar(250),
		Answer varchar(250)
		)""");
cur.execute("""
	CREATE TABLE hospital_reviews(
		ID int IDENTITY(1,1) PRIMARY KEY,
		ProviderID int,
		SurveyID varchar(100),
		AnswerPercent int,
		CompletedServeys varchar(100),
		ResponseRate int,
		Footnote int,
		StartDate date,
		EndDate date
	)""");

############################################
##	Add Data to Hospital Reviews	  ##
############################################
success = 0
fail = 0
for value in table:
	cur.execute("""
		INSERT INTO hospital_reviews(ProviderID, SurveyID, AnswerPercent, CompletedServeys, ResponseRate, Footnote, StartDate, EndDate) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
		""", (value[0], value[8], value[11], value[12], value[13], value[14], value[15], value[16]))  
for value in table:
	try:
		cur.execute("""
			INSERT INTO HCAHPSMeasure(ID, Question, Answer) VALUES(?, ?, ?) 
			""", (value[8], value[9], value[10]))
		success += 1
	except: 
		fail += 1
print "Out of %d attempts, there were %d successes and %d duplicates" %(success + fail, success, fail)
con.commit()


