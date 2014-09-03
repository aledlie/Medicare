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

print "\nNumber of reviews in the hospital reviews table:"
cur.execute("SELECT COUNT(*) FROM hospital_reviews")
print cur.fetchone()

print "\nNumber of providers reviewed:"
cur.execute("SELECT COUNT(*) FROM Providers")
print cur.fetchone()

print "\nNumber of Outpatient procedures for which provider cost information is availible:"
#cur.execute("SELECT COUNT(*) FROM outpatientprocedures")	

def table_info(name):
	print "\nTable Name: %s" %name
	print "Col Name \t\t Data Type"
	print "------------------------------------------"
	rows = cur.execute("PRAGMA table_info(Providers)").fetchall()
	for row in rows:
		print "%-25s %s" %(row[1], row[2]) 
########################################
###	Get Table Data 		     ###
########################################
table_info('Providers')
print "\nTable Name: HCAHPSMeasure"
print "Col Name \t\t  Data Type"
print "-----------------------------------------"
rows = cur.execute("PRAGMA table_info(HCAHPSMeasure)").fetchall()
for row in rows:
	print "%-25s %s" %(row[1], row[2])

print "\nTable Name: hospital_reviews"
print "Col Name \t\t  Data Type"
print "-----------------------------------------"
rows = cur.execute("PRAGMA table_info(hospital_reviews)").fetchall()
for row in rows:
	print "%-25s %s" %(row[1], row[2])

###########################################
###		Query Reviews 		###
###########################################

cur.execute("SELECT ID, Name FROM Providers WHERE HospitalReferralRegion = 'TX - Austin'")
print cur.fetchall()


rows = cur.execute("""
		SELECT hospital_reviews.SurveyID, HCAHPSMeasure.Question, HCAHPSMeasure.Answer 
		FROM HCAHPSMeasure 
		INNER JOIN hospital_reviews
		ON hospital_reviews.SurveyID = HCAHPSMeasure.ID
		""").fetchall()
rows = cur.execute("SELECT * FROM HCAHPSMeasure")
for row in rows:
	print row

print "\nWhere the highest percent of patients would \"definitely\" recommend the hospital (w/ 300+ responses)\n" 
rows = cur.execute("""
			SELECT Providers.Name, Providers.City, Providers.State, AVG(hospital_reviews.AnswerPercent)
			FROM HCAHPSMeasure 
			INNER JOIN hospital_reviews
			On hospital_reviews.SurveyID = HCAHPSMeasure.ID
			INNER JOIN Providers
			ON Providers.ID = hospital_reviews.ProviderID
			WHERE hospital_reviews.SurveyID = 'H_RECMND_DY' AND hospital_reviews.completedserveys = '300 or more'
			GROUP BY Providers.Name
			ORDER BY AVG(hospital_reviews.AnswerPercent) DESC
			Limit 20
			""").fetchall()

for row in rows:
	print row


print "\nWhere the highest percent of patients would \"definitely\" or \"probably\" recommend the hospital (w/ 300+ responses)\n" 
rows = cur.execute("""
			SELECT Providers.Name, Providers.City, Providers.State, SUM(hospital_reviews.AnswerPercent)
			FROM HCAHPSMeasure 
			INNER JOIN hospital_reviews
			On hospital_reviews.SurveyID = HCAHPSMeasure.ID
			INNER JOIN Providers
			ON Providers.ID = hospital_reviews.ProviderID
			WHERE (hospital_reviews.SurveyID = 'H_RECMND_DY' OR hospital_reviews.SurveyID = 'H_RECMND_PY') AND hospital_reviews.completedserveys = '300 or more'
			GROUP BY Providers.Name
			ORDER BY AVG(hospital_reviews.AnswerPercent) DESC
			Limit 20
			""").fetchall()

for row in rows:
	print row
