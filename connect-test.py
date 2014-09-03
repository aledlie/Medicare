#connect to ESP database
import pyodbc as p
con1 = p.connect("DSN=sqlserver01;UID=admin;PWD=asc@dm1n")

#import library to connect to .csv file
import csv

#open cursor
cursor = con1.cursor()

#get data from SQLServer test
cursor.execute("SELECT Name FROM Employee")
rows = cursor.fetchall()
for row in rows:
	#print row.Name

#get data from .csv file test
with open('/Users/alyshialedlie/Downloads/CompleteProjectIndex.csv', 'r') as myfile:
	rows = csv.reader(myfile, delimiter=' ', quotechar='"')
		for row in rows:
			print row
	#con1.commit()
	myfile.close()



#get data from .csv file test
#with open('/Users/alyshialedlie/Downloads/CompleteProjectIndex.csv','r') as myfile:
#	rows = csv.reader(myfile, delimiter=',', quotechar='"')
#		for row in rows:
#		insert_str = 'INSERT into raw_data VALUES(something, something)'
#		print insert_str
#		#crsr.execute(insert_str)
#   	#cnxn.commit()
#    	myfile.close()

