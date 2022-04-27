#!/usr/bin/python3

# Module Imports
import os
import mariadb
import sys
import csv
from datetime import datetime
from dateutil.parser import *



# Open Connection with MariaDB
try:
    conn = mariadb.connect(
    user="jroco",
    password="qwerty",
    host="131.221.33.50",
    port=3306,
    database="company"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
# Get Cursor
cur = conn.cursor()
#cur.close()

# Create file to record unformat input records

filej= 'job_error.txt'
filed= 'department_error.txt'
filee= 'employee_error.txt'

try:
    os.remove("job_error.txt")
    os.remove("department_error.txt")
    os.remove("employee_error.txt")
except:
    pass

try:
    file_job = open(filej, 'a')
    file_depart = open(filed, 'a')
    file_emplo = open(filee, 'a')
except:
    pass


# Load Jobs
with open('jobs.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    for row in csv_reader:
        try:
            # Here we can limit the lines to load
            print("INSERT INTO company.job values(",row[0],",'",row[1],"');")
            query = f"INSERT INTO company.job values('{row[0]}','{row[1]}')"
            cur.execute(query)
            print(f"{cur.rowcount} details inserted")
            conn.commit()
        except Exception as e:
            print(line_count,row[2]," WARNING ",e)
            string01 = str(row) + " " + str(e) + "\n"
            file_job.write(string01)
            pass
        line_count = line_count + 1
# Load Department
with open('departments.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    for row in csv_reader:
        try:
            # Here we can limit the lines to load
            print("INSERT INTO company.department values(",row[0],",'",row[1],"');")
            query = f"INSERT INTO company.department values('{row[0]}','{row[1]}')"
            cur.execute(query)
            print(f"{cur.rowcount} details inserted")
            conn.commit()
        except Exception as e:
            print(line_count,row[2]," WARNING ",e)
            string01 = str(row) + " " + str(e) + "\n"
            file_depart.write(string01)
            pass
        line_count = line_count + 1
# Load Employees
with open('hired_employees.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    for row in csv_reader:
        try:
            now = parse(row[2])
            print("INSERT INTO company.employee values(",row[0],",'",row[1],"','",now.strftime("%y-%m-%d %H:%M:%S"),"',",row[3],",",row[4],");")
            date01=now.strftime("%y-%m-%d %H:%M:%S")
            query = f"INSERT INTO company.employee values('{row[0]}','{row[1]}','{date01}','{row[3]}','{row[4]}')"
            cur.execute(query)
            print(f"{cur.rowcount} details inserted")
            conn.commit()
        except Exception as e:
            print(line_count+1,row[2]," WARNING ",e)
            string01 = str(row) + " " + str(e) + "\n"
            file_emplo.write(string01)
            pass
        line_count = line_count + 1

cur.close()
file_job.close()
file_depart.close()
file_emplo.close()
