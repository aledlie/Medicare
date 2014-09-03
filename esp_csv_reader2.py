#import libraries 
import csv
import sys
import pyodbc as p
import re
import string
from datetime import datetime 

#connect to ESP database and open cursor
con1 = p.connect("DSN=sqlserver01;UID=admin;PWD=asc@dm1n")
cursor = con1.cursor()

#initialize variables
rownum = 0
FILTER_COLUMNS = ('ClientName', 'ProjectName')
client = ''
pm = ''
project = ''
comments = ''
table = []

#Create temp table
cursor.execute("IF OBJECT_ID('temp', 'U') IS NOT NULL DROP TABLE temp;")
cursor.execute("""
		CREATE TABLE temp(
			ProjectName varchar(100),
			ClientName varchar(50),
			ProjectManager varchar(50),
			PointOfContact varchar(50),
			StartDate date,
			EndDate date,
			Is_Complete bit,
			Comments varchar(750)
		);
		""")


#Read from .csv file into Key-Value mapping 'table'
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
				print '%s: %d: %s' % (header[colnum], colnum, col)
				#print '%-8s: %s' % (header[colnum], col)
				L.append(col)
				if colnum == 0:
					client = col
				if colnum == 1:
					project = col
				if colnum == 2:
					comments = col					
				colnum += 1
		table.append(L)
		rownum += 1
finally:
	f.close()

#method to check for date values in table
def valid_date(datestring):
	try: 
		datetime.strptime(datestring, '%m/%d/%y')
		return True
	except ValueError:
		return False


#iterate through key-value mappings and format entries
for value in table:
	for i in range (len(value)):
		if i == 6:
			if value[i] == 'Active':
				value[i] = 1
			else:
				value[i] = 0
		if i in (3, 4):
			employee = string.split(value[i])
			if len(employee) == 2:
				employee1 = string.lower(employee[0][0]) + employee[1]
				employee1 = employee1.replace('\'', '')
				value[i] = employee1
			if len(employee) == 3:
				employee1 = string.lower(employee[0][0]) + employee[2]
				value[i] = employee1
		if i in (8, 9):
			print "%d: %s" %(i, value[i])
			if valid_date(str(value[i])): 
				print "%d: %s" %(i, value[i])
				date = datetime.strptime(str(value[i]), '%m/%d/%y') 
				value[i] = date.strftime('%Y-%m-%d')			
			else :
				value[i] = ''

#insert Clients into Clients table
for i in range (len(table)):
	if i != 0:
		try: 
			cursor.execute("INSERT INTO Client(Name) VALUES(?)", table[i][0])
			print 'The Client %s was insterted into the database' % str(table[i][0]) 
			#cursor.commit()
		except:
			message = "Error: Duplicate Client Name"
			#print message

#insert Employees int Employee table
for i in range (len(table)):
	if i != 0:
		employee1 = table[i][3]
		email = employee1 + '@accesssciences.com'
		#print email
		try: 
			cursor.execute("""
				INSERT INTO Employee(username, Name, IsCurrentEmployee, EMAIL) VALUES(?, ?, ?, ?)	
				""", employee1, table[i][3], 1, email)
			#cursor.commit()
 			print "Inserted into ESP: %s, %s, %s" %(employee1, table[i][3], 1, email)
		except:
			message = "Error" 
			#print message


#insert into temp SQL Table
success = 0
fail = 0
for i in range (len(table)):
	if i != 0:
		try:	
			cursor.execute("""
				INSERT INTO ProjectIndex(ClientName, ProjectName, Is_Complete, Comments, StartDate, EndDate, ProjectManager, PointOfContact) 
				VALUES(?, ?, ?, ?, ?, ?, ?, ?)
				""", table[i][0], table[i][1], table[i][7], table[i][2], table[i][9], table[i][10], table[i][3], table[i][4]) 
			success = success + 1
			#cursor.commit()
			#print " %s: %s was inserted into ESP: StartDate: %s, EndDate: %s, PM: %s, POC: %s" %(table[i][0], table[i][1], table[i][9], table[i][10], table[i][3],table[i][4])
		except:
			fail = fail + 1
			#print "Error: Client: %s, Project: %s PM: %s, PoC; %s" %(table[i][0], table[i][1], table[i][3], table[i][4])

print "Out of %d attempted inserts, there were %d successes and %d failures.\n" %(success + fail, success, fail)
#for row in cursor.execute("SELECT * FROM temp"):
#	print row

#Update All Commments
#initialize variables to keep track of fail rate
success = 0
fail = 0
#Test
#client = table[1][0]
#project = table[1][1]
#cursor.execute("SELECT * FROM ProjectIndex WHERE ClientName = ? AND ProjectName = ?", client, project)
#row = cursor.fetchall()
#print row

#loop through all rows in table, skipping header row
count = 0
for i in range (len(table)):
	if i != 0:
		client = table[i][0]
		project = table[i][1]
		comments = table[i][2]
		startDate = table[i][8]
		endDate = table[i][9]
		print "%s: %s, %s-%s" %(client, project, startDate, endDate)	
		try:
			#cursor.execute("SELECT * FROM ProjectIndex WHERE ClientName = ? AND ProjectName = ?", client, project) 
			cursor.execute("UPDATE ProjectIndex SET Comments = ? WHERE ClientName = ? AND ProjectName = ?", comments, client, project)	
			cursor.execute("UPDATE ProjectIndex SET startdate = ? WHERE ClientName = ? AND ProjectName = ?", startDate, client, project)
			cursor.execute("UPDATE ProjectIndex SET enddate = ? WHERE ClientName = ? AND ProjectName = ?", endDate, client, project)
			success = success + 1
		except:
			fail = fail + 1
			print "Error"
cursor.commit()
cursor.close()
print "Out of %d attempts, %d Comments were successfully updated and %d failed." %(fail + success, success, fail)









