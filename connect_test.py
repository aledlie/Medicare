import pyodbc as p

#connect to databse using ODBC string
cnxn = p.connect("driver='{SQL Server}' Server=192.168.0.26; Initial Catalog=projectindex; User ID=admin;password=asc@dm1n")
