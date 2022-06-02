import sqlite3
import csv


connection = sqlite3.connect('pythonAssignment.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS TrainingData
              (X TEXT, Y1  TEXT, Y2 TEXT,Y3 TEXT,Y4 TEXT )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS IdealFunctions
              (X TEXT, Y1  TEXT, Y2 TEXT,Y3 TEXT,Y4 TEXT,Y5 TEXT,Y6 TEXT
              ,Y7 TEXT,Y8 TEXT,Y9 TEXT,Y10 TEXT,Y11 TEXT,Y12 TEXT,Y13 TEXT,Y14 TEXT, Y15 TEXT,Y16 TEXT,Y17 TEXT,Y18 TEXT
              ,Y19 TEXT,Y20 TEXT,Y21 TEXT,Y22 TEXT,Y23 TEXT,Y24 TEXT,Y25 TEXT,Y26 TEXT,Y27 TEXT,Y28 TEXT,Y29 TEXT
              ,Y30 TEXT,Y31 TEXT,Y32 TEXT,Y33 TEXT,Y34 TEXT,Y35 TEXT,Y36 TEXT,Y37 TEXT,Y38 TEXT,Y39 TEXT,Y40 TEXT
              ,Y41 TEXT,Y42 TEXT,Y43 TEXT,Y44 TEXT,Y45 TEXT,Y46 TEXT,Y47 TEXT,Y48 TEXT,Y49 TEXT,Y50 TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS TestData
              (X TEXT, Y  TEXT)''')

# Opening the train.csv file
file = open('train.csv')
file1 = open('ideal.csv')
file2 = open('test.csv')

# Reading the contents of the
# train.csv file
contents = csv.reader(file)
contents1 = csv.reader(file1)
contents2 = csv.reader(file2)

# SQL query to insert data into the
# trainingData table
insert_records = "INSERT INTO TrainingData (X,Y1,Y2,Y3,Y4) VALUES(?,?,?,?,?)"
insert_records1 = "INSERT INTO IdealFunctions (x,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14,y15,y16,y17,y18,y19,y20,y21,y22,y23,y24,y25,y26,y27,y28,y29,y30,y31,y32,y33,y34,y35,y36,y37,y38,y39,y40,y41,y42,y43,y44,y45,y46,y47,y48,y49,y50) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
insert_records2 = "INSERT INTO TestData (X,Y) VALUES(?,?)"

# Importing the contents of the file
# into our TrainingData table
cursor.executemany(insert_records, contents)
cursor.executemany(insert_records1, contents1)
cursor.executemany(insert_records2, contents2)

cursor.execute('SELECT COUNT(*) from TrainingData')
trainingData_count = cursor.fetchone()

cursor.execute('SELECT COUNT(*) from IdealFunctions')
idealFunction_count = cursor.fetchone()


cursor.execute('SELECT COUNT(*) from TestData')
testData_count = cursor.fetchone()

# SQL query to retrieve all data from
# the TrainingData table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM TrainingData"
rows = cursor.execute(select_all).fetchall()

select_all1 = "SELECT * FROM IdealFunctions"
rows1 = cursor.execute(select_all1).fetchall()

select_all2 = "SELECT * FROM TestData"
rows2 = cursor.execute(select_all2).fetchall()
 
# Output to the console screen
for r in rows:
    print(r)

for r in rows1:
    print(r)

for r in rows2:
    print(r)

print(trainingData_count)
print(idealFunction_count)
print(testData_count)


connection.commit()
connection.close()