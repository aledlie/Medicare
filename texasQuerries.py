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

def printTable(cur):
	rows = cur.fetchall()
	print "%-45s %-15s %-20s" %("Hospital Name", "City", "Average Cost")	
	print "----------------------------------------------------------------------------------"
	for row in rows:
		print "%-45s %-15s %-20.2f" %(row[0], row[1], row[2])

def printTable2(cur):
	rows = cur.fetchall()
	print "%-45s %-15s %-65s %-15s" %("Hospital Name", "City", "Procedure Type", "Average Cost")
	print "------------------------------------------------------------------------------------------------------------------------------------------------"
	for row in rows:	
		temp = row[2].split("-")
		temp = limit(temp[1], 65)
		print "%-45s %-15s %-65s %-15.2f" %(row[0], row[1], temp, row[3])
def limit(s, l):
	if len(s) <= l:
		return s
	else:
		return s[0:l-3] + '...'

#################################
##			       ##	
## Playing with Data!	       ##
##			       ##	
#################################
cur.execute("PRAGMA table_info('OutpatientVisits')")
print cur.fetchall()

print "\nThe Most Expensive Procedure Locations (actually paid - Medicare)\n"
cur.execute("""
SELECT Providers.Name, Providers.City, OutpatientVisits.APC, MAX(OutPatientVisits.AverageTotalPayments) 
FROM OutPatientVisits
INNER JOIN Providers
ON Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY OutPatientVisits.APC
""")
printTable2(cur)

print "\nThe Least Expensive Procedure Locations (acutally paid - Medicare)\n"
cur.execute("""
SELECT Providers.Name, Providers.City, OutpatientVisits.APC, MIN(OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER JOIN Providers
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY OutPatientVisits.APC
""")
printTable2(cur)

print "\nThe Least Expensive Procedure Locations (billed)\n"
cur.execute("""
SELECT Providers.Name, Providers.City, OutpatientVisits.APC, MIN(OutPatientVisits.AverageSubmittedCharges)
FROM OutPatientVisits
INNER Join Providers
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY OutPatientVisits.APC
""")
printTable2(cur)

print "\nThe Most Expensive Procedure Locations (billed)\n"
cur.execute("""
SELECT Providers.Name, Providers.City, OutpatientVisits.APC, MAX(OutPatientVisits.AverageSubmittedCharges)
FROM OutPatientVisits
INNER Join Providers
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY OutPatientVisits.APC
""")
printTable2(cur)

print "\nThe Largest Disparity\n"
cur.execute("""
SELECT Providers.Name, Providers.City, OutpatientVisits.APC, OutPatientVisits.AverageSubmittedCharges, OutPatientVisits.AverageTotalPayments, MAX(OutPatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER JOIN Providers
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY OutPatientVisits.APC
ORDER BY MAX(OutpatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments) DESC
""")

rows = cur.fetchall()
print "%-45s %-20s %-50s %-15s %-15s %-15s" %("Hospital Name", "City", "Procedure Type", "Submitted Charge", "Ammount Payed", "Difference")
for row in rows:	
	temp = row[2].split("-")
	temp = limit(temp[1], 50)
	print "%-45s %-20s %-50s %-15.2f %-15.2f %-15.2f" %(row[0], row[1], temp, row[3], row[4], row[5])



print "\nAverage Expense of Uninsured Hospital Visit - By Hosptial in Austin, TX\n"
cur.execute("""
SELECT Providers.Name, Providers.City, AVG(OutpatientVisits.AverageSubmittedCharges)
FROM Providers
INNER JOIN OutpatientVisits
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY Providers.Name
ORDER BY AVG(OutpatientVisits.AverageSubmittedCharges) ASC
""")
printTable(cur)

print "\nAverage Expense of Medicare Insured Hospital Visit - By Hospital in Austin, TX\n"
cur.execute("""
SELECT Providers.Name, Providers.City, AVG(OutpatientVisits.AverageTotalPayments)
FROM Providers
INNER JOIN OutpatientVisits
ON Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Austin'
GROUP BY Providers.Name
ORDER BY AVG(OutpatientVisits.AverageTotalPayments) ASC
""")
printTable(cur)

print "\nAverage Expense of Uninsured Outpaitent Hospital Visit - By Hospital in Houston, TX\n"
cur.execute("""
SELECT Providers.Name, Providers.City, AVG(OutpatientVisits.AverageSubmittedCharges)
FROM Providers
INNER JOIN OutpatientVisits
On Providers.ID = OutPatientVisits.ProviderID
WHERE Providers.HospitalReferralRegion = 'TX - Houston'
GROUP BY Providers.Name
ORDER BY AVG(OutpatientVisits.AverageSubmittedCharges) ASC
""")
printTable(cur)
