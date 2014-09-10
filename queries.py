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

def limit(s, l):
	if len(s) <= l:
		return s
	else:
		return s[0:l-3] + '...'

def printTable(cur):
	table = cur.fetchall()
	for row in table:
		str = ''
		rownum = 0
		for value in row:	
			if type(value) in (float, int):
				temp = "%-10.2f" %value
			else:	
				if len(value) < 5:
					temp = "%-10s" %value	
				else:
					temp = "%-45s" %limit(value, 45)			
			if rownum == 1:
				temp = "%-20s" %value
			str = str + temp
			rownum += 1
		print str

#################################
##			       ##	
## Playing with Data!	       ##
##			       ##	
#################################

# Find Most Expensive Hospitals Nationally, by Procedure
cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientServices.Description, MAX(OutPatientVisits.AverageTotalPayments), AVG(OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER JOIN Providers
ON Providers.ID = OutPatientVisits.ProviderID
INNER JOIN OutpatientServices
ON OutpatientVisits.APCID = OutpatientServices.ID
GROUP BY OutPatientVisits.APCID
ORDER BY MAX(OutpatientVisits.AverageTotalPayments) DESC
""")

print "\nThe Most Expensive Procedure Locations (total payments)\n"
print "%-44s %-19s %-9s %-44s %-10s %-10s" %("Hospital", "City", "State", "Procedure", "Cost", "National Average")
print "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
printTable(cur)

# Find 
print "\nThe Least Expensive Procedure Locations (total payments)\n"
cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientServices.Description, MIN(OutPatientVisits.AverageTotalPayments), AVG(OutpatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER Join Providers
On Providers.ID = OutPatientVisits.ProviderID
INNER JOIN OutpatientServices
ON OutPatientVisits.APCID = OutPatientServices.ID
GROUP BY OutPatientVisits.APCID
ORDER BY MIN(OutpatientVisits.AverageTotalPayments) ASC/""")
print "%-45s %-19s %-9s %-44s %-10s %-10s" %("Hospital", "City", "State", "Procedure", "Cost", "National Average")
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------"
printTable(cur)

print "\nThe Largest Disparities Between Charges and Payments\n"
cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientServices.Description, OutPatientVisits.AverageSubmittedCharges, OutPatientVisits.AverageTotalPayments, MAX(OutPatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER JOIN Providers
On Providers.ID = OutPatientVisits.ProviderID
INNER JOIN OutpatientServices
ON OutpatientVisits.APCID = OutpatientServices.ID
GROUP BY OutPatientVisits.APCID
ORDER BY MAX(OutpatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments) DESC
""")
print "%-45s %-19s %-9s %-44s %-10s %-10s %-10s" %("Hospital", "City", "State", "Procedure", "Charged", "Reimbursed", "Disparity")
print "-------------------------------------------------------------------------------------------------------------------------------------------------------------"
printTable(cur)


cur.execute("Select Count(*) From Providers")
print  cur.fetchone()
cur.execute("Select Count(*) From Outpatientvisits")
print cur.fetchone()
