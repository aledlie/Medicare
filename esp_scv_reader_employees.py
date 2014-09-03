#import libraries 
import csv
import sys
import pyodbc as p
import re
import string
import itertools
from datetime import datetime 

##############################################
## connect to ESP database and open cursor  ##
##############################################

con1 = p.connect("DSN=sqlserver01;UID=admin;PWD=asc@dm1n")
cursor = con1.cursor()

#initialize variables
rownum = 0
table = []

#Drop temp table
#cursor.execute("IF OBJECT_ID('temp', 'U') IS NOT NULL DROP TABLE temp;")

########################################################
## Read from .csv file into Key-Value mapping 'table' ##
########################################################

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
				if colnum < 5:
					print '%s: %d: %s' % (header[colnum], colnum, col)
					#print '%-8s: %s' % (header[colnum], col)
					L.append(col)
					colnum = colnum + 1
		print "\n"
		table.append(L)
		rownum += 1
finally:
	f.close()

##############################################
##  Python Formating Methods - called later ##
##############################################

#method to check for date values in table
def valid_date(datestring):
	try: 
		datetime.strptime(datestring, '%m/%d/%y')
		return True
	except ValueError:
		return False

#method to get username from name
def get_username(name):
	name = name.replace('\'', '')
	name_split = string.split(name);
	if len(name_split) > 1:
		username = string.lower(name_split[0][0]) + name_split[len(name_split) - 1]
		return username
	else:
		return name

##############################################
## iterate through table and format entries ##
##############################################	
for i in range (len(table)):
	if i != 0:
		username = get_username(table[i][0])
		man_username = get_username(table[i][3])
		table[i][2] = username
		table[i][3] = man_username
		if table[i][1] == 'Foundations':
			table[i][1] = 'Foundations - Red'

# Loop over the entries in the table, popping shit (and/or locking shit) like its hawt.

#print formated table
for value in table:
	for i in range (len(value)):
		print "%d: %s" %(i, value[i])
	print "\n"

###########################################
##  insert Employees int Employee table  ##
###########################################
success = 0
fail = 0
for i in range (len(table)):
	if i != 0:
		employee1 = table[i][2]
		email = employee1 + '@accesssciences.com'	
		try:
			cursor.execute("SELECT ID FROM Community WHERE Name = ?", table[i][1])
			community = cursor.fetchone()[0]
			#print community
		except:
			print "Error: Cound not get Community: %s" %(table[i][1])
#		try: 
#			cursor.execute("""
#				INSERT INTO Employee(username, Name, IsCurrentEmployee, Manager, email, jobtitle, community) VALUES(?, ?, ?, ?, ?, ?, ?)	
#				""", table[i][2], table[i][0], 1, table[i][3], email, table[i][4], community)
#			cursor.commit()
#			success = success + 1
#			print "Inserted into ESP: %s, %s, %s, %s, %s, %s" %(table[i][0], table[i][2], 1, table[i][3], email, table[i][4])
#		except:
#			fail = fail + 1
#			message = "Error: %s was not inserted" %table[i][0] 
#			print message

############################################
##     Update Employees 		  ##
############################################
for i in range (len(table)):
	if i != 0:
		try:
			success = success + 1
			cursor.execute("SELECT ID FROM Community WHERE Name = ?", table[i][1])
			community = cursor.fetchone()[0]
			cursor.execute("UPDATE Employee SET Community = ? WHERE username = ?", community, table[i][2])
			cursor.commit();
			cursor.execute("UPDATE Employee SET jobtitle = ? WHERE username = ?", table[i][4], table[i][2])
			cursor.commit();
			cursor.execute("UPDATE Employee SET Manager = ? WHERE username = ?", table[i][3], table[i][2])
			cursor.commit();
		except: 
			fail = fail + 1
			print "Updating community of %s failed." %table[i][0]


#insert into temp SQL Table
#for i in range (len(table)):
#	if i != 0:
#		try:	
#			cursor.execute("""
#				INSERT INTO ProjectIndex(ClientName, ProjectName, Is_Complete, Comments, StartDate, EndDate, ProjectManager, PointOfContact) 
#				VALUES(?, ?, ?, ?, ?, ?, ?, ?)
#				""", table[i][0], table[i][1], table[i][7], table[i][2], table[i][9], table[i][10], table[i][3], table[i][4]) 
#			success = success + 1
#			#cursor.commit()
#			#print " %s: %s was inserted into ESP: StartDate: %s, EndDate: %s, PM: %s, POC: %s" %(table[i][0], table[i][1], table[i][9], table[i][10], table[i][3],table[i][4])
#		except:
#			fail = fail + 1
#			#print "Error: Client: %s, Project: %s PM: %s, PoC; %s" %(table[i][0], table[i][1], table[i][3], table[i][4])

print "Out of %d attempted inserts, there were %d successes and %d failures.\n" %(success + fail, success, fail)
#for row in cursor.execute("SELECT * FROM temp"):
#	print row



#################################
##			       ##	
## Update ProjectIndex Fields  ##
##			       ##	
#################################


#initialize variables to keep track of fail rate
success = 0
fail = 0

#loop through all rows in table, skipping header row
#count = 0
#for i in range (len(table)):
#	if i != 0:
#		client = table[i][0]
#		project = table[i][1]
#		comments = table[i][2]
#		isComplete = table[i][6]
#		startDate = table[i][8]
#		endDate = table[i][9]
#		print "%s: %s, %s-%s" %(client, project, startDate, endDate)	
#		try:
#			#cursor.execute("SELECT * FROM ProjectIndex WHERE ClientName = ? AND ProjectName = ?", client, project) 
#			cursor.execute("UPDATE ProjectIndex SET Comments = ? WHERE ClientName = ? AND ProjectName = ?", comments, client, project)	
#			cursor.execute("UPDATE ProjectIndex SET startdate = ? WHERE ClientName = ? AND ProjectName = ?", startDate, client, project)
#			cursor.execute("UPDATE ProjectIndex SET enddate = ? WHERE ClientName = ? AND ProjectName = ?", endDate, client, project)
#			cursor.execute("UPDATE ProjectIndex SET IsComplete = ? WHERE ClientName = ? AND ProjectName = ?", isComplete, client, project)
#			success = success + 1
#		except:
#			fail = fail + 1
#			print "Error"
#cursor.commit()
#cursor.close()
#print "Out of %d attempts, %d Comments were successfully updated and %d failed." %(fail + success, success, fail)









