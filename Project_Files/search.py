####step 1: import all modules and fucntions
import pandas as pd
import sys
import os


####step 2: get all details of student ( name, individual marks, total marks, percentile, grade, exam analysis, )
roll_no=sys.argv[1]
# print(roll_no)
data=pd.read_csv('main.csv')
Roll_no2=roll_no.lower()
Roll_no1=roll_no.upper()
individual_marks1 = data[data['Roll_Number']==Roll_no1]
individual_marks2 = data[data['Roll_Number']==Roll_no2]
if individual_marks1.empty:
    print(individual_marks2)
else:
    print(individual_marks1)