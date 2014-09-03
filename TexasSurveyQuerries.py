import sqlite3
con = sqlite3.connect("MedicareData.db")
cur = con.cursor()

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
			AND Providers.HospitalReferralRegion = 'TX - Houston'
			GROUP BY Providers.Name
			ORDER BY AVG(hospital_reviews.AnswerPercent) DESC
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
			WHERE (hospital_reviews.SurveyID = 'H_RECMND_DY' OR hospital_reviews.SurveyID = 'H_RECMND_PY') AND hospital_reviews.completedserveys = '300 or more'			      AND Providers.HospitalReferralRegion = 'TX - Houston'
			GROUP BY Providers.Name
			ORDER BY AVG(hospital_reviews.AnswerPercent) DESC
			""").fetchall()

for row in rows:
	print row
