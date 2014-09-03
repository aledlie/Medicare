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

#################################
##			       ##	
## Playing with Data!	       ##
##			       ##	
#################################

cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientVisits.APC, MAX(OutPatientVisits.AverageTotalPayments) 
FROM OutPatientVisits
INNER Join Providers
ON Providers.ID = OutPatientVisits.ProviderID
GROUP BY OutPatientVisits.APC
""")

print "\nThe Most Expensive Procedure Locations\n"
rows = cur.fetchall()
for row in rows:
	print row

print "\nThe Least Expensive Procedure Locations\n"
cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientVisits.APC, MIN(OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER Join Providers
On Providers.ID = OutPatientVisits.ProviderID
GROUP BY OutPatientVisits.APC
ORDER BY MIN(OutPatientVisits.AverageTotalPayments) ASC
""")

rows = cur.fetchall()
for row in rows:
	print row


print "\nThe Largest Disparities Between Charges and Payments\n"
cur.execute("""
SELECT Providers.Name, Providers.City, Providers.State, OutpatientVisits.APC, OutPatientVisits.AverageSubmittedCharges, OutPatientVisits.AverageTotalPayments, MAX(OutPatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments)
FROM OutPatientVisits
INNER JOIN Providers
On Providers.ID = OutPatientVisits.ProviderID
GROUP BY OutPatientVisits.APC
ORDER BY MAX(OutpatientVisits.AverageSubmittedCharges - OutPatientVisits.AverageTotalPayments) DESC
""")
rows = cur.fetchall()
for row in rows:
	print row
