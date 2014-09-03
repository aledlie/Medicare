#import libraries 
import csv
import sys
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
providers = []
services = []

#method to get procedure ID
def getID(name):
	name = name.split('-')
	name[0] = name[0].strip()
	return name[0]

#get procedure name
def getName(name):
	name = name.split('-')
	name[1] = name[1].strip()
	return name[1]

#method to get username from name
def get_username(name):
	name = name.replace('\'', '')
	name_split = string.split(name);
	if len(name_split) > 1:
		username = string.lower(name_split[0][0]) + name_split[len(name_split) - 1]
		return username
	else:
		return name

def printTable(table):
	for row in table:
		rownum = 0
		print "\n"
		for i in row:
			print "%d: %s" %(rownum, i)
			rownum += 1


#########################################################
## Read from .csv file into Key-Value mapping 'tables' ##
#########################################################

f = open(sys.argv[1], 'rt')
try:
	dialect = csv.excel()	
	reader = csv.reader(f, dialect)
	#read in .csv file, store in 2D array
	for row in reader:
		L1 = []
		L2 = []
		#Save header row
		if rownum == 0:
			header = row
		else:
			colnum = 0	
			for col in row:
				#print '%s: %d: %s' % (header[colnum], colnum, col)
				if colnum in (1, 2, 3, 4, 5, 6, 7):
					L1.append(col)
				if colnum in (1, 0, 8, 9, 10):
					if colnum == 0:
						procedureID = getID(col)
						description = getName(col)
						L2.append(procedureID)
						L2.append(description)
					else:
						L2.append(col)
				colnum = colnum + 1
		print "\n"
		if (len(L1) > 0):
			providers.append(L1)
		if (len(L2) > 0):
			services.append(L2)
		rownum = rownum + 1
		count  = count + 1
finally:
	f.close()

print "There are %d total entries" %(count)

#dump provider information to SQL table
success = 0
fail = 0
for value in providers:
	try:
		cur.execute("""
			INSERT INTO Providers VALUES(?, ?, ?, ?, ?, ?, ?)
			""", (value[0], value[1], value[2], value[3], value[4], value[5], value[6]))
		success += 1
	except: 
		fail += 1
		message = "There was an error"
		#print message
print "Out of %d attempts, there were %d providers inserted and %d duplicates" %(fail + success, success, fail)

#print number of providrs inserted into SQL table
cur.execute("SELECT Count(*) FROM Providers") 	
print cur.fetchone()

#printTable(services)
#Insert values into table
success = 0
fail = 0
for value in services:
	try:	
		cur.execute("""
			INSERT INTO OutpatientVisits(APCID, ProviderID, OutpatientServices, AverageSubmittedCharges, AverageTotalPayments, Year) VALUES(?, ?, ?, ?, ?, 2011)
			""", (value[0], value[2], value[3], value[4], value[5]))
		success += 1
	except:
		message = "There was an error inserting into the services table"
		fail += 1
		#print message
print "Out of %d insertion attempts for the services table, there were %d successes and %d failures" %(success + fail, success, fail)
#save changes
con.commit()

