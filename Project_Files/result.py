####step 1: import all modules and fucntions
import pandas as pd
import sys
import os
from matplotlib import pyplot as plt
from abs import grade_boundaries, count,mean_score,std_dev,high
import numpy as np
print("===============GENERATING REPORT CARD=================")
print('''
                      ___..............._
             __.. ' _'.""""""\\""""""""- .`-._
 ______.-'         (_) |      \\           ` \\`-. _
/_       --------------'-------\\---....______\\__`.`  -..___
| T      _.----._           Xxx|x...           |          _.._`--. _
| |    .' ..--.. `.         XXX|XXXXXXXXXxx==  |       .'.---..`.     -._
\_j   /  /  __  \  \        XXX|XXXXXXXXXXX==  |      / /  __  \ \        `-.
 _|  |  |  /  \  |  |       XXX|""'            |     / |  /  \  | |          |
|__\_j  |  \__/  |  L__________|_______________|_____j |  \__/  | L__________J
     `'\ \      / ./__________________________________\ \      / /___________\
        `.`----'.'   dp                                `.`----'.'
          `""""'                                         `""""'
''')

####step 2: get all details of student ( name, individual marks, total marks, percentile, grade, exam analysis, )
##getting name and individual marks
roll_no=sys.argv[1]
data=pd.read_csv('main.csv')
roll_no1=roll_no.upper()
roll_no2=roll_no.lower()
marks1 = data[data['Roll_Number']==roll_no1]
marks2 = data[data['Roll_Number']==roll_no2]
if marks1.empty:
    marks=marks2
else:
    marks=marks1
i=1
individual_marks=dict()
for el in marks:
    if(i==2):
        name=marks[el].to_string(index=False)
    elif(i>=3):
        individual_marks[el]=marks[el].to_string(index=False)
    i=i+1

###getting percentile
total_s=0
lower_s=0
# print(data['total'])
# print(individual_marks)
total_marks=float(individual_marks['total'])
for m in data['total']:
    if(total_marks>=(m)):
        lower_s=lower_s+1
    total_s=total_s+1
percentile=lower_s*100/total_s
rank=total_s-lower_s+1
# print(percentile)
####getting grades
grade=pd.read_csv('grades.txt')
roll_no1=roll_no.upper()
roll_no2=roll_no.lower()
grade_data1 = grade[grade['Roll_Number']==roll_no1]
grade_data2 = grade[grade['Roll_Number']==roll_no2]
if grade_data1.empty:
    grade_data=grade_data2
else:
    grade_data=grade_data1
Grade=grade_data['Grade'].to_string(index=False)

####getting exam analysis
def ana(file):
    file_extension = os.path.splitext(file)[1]
    if(file_extension!=".csv"):
        file=file+".csv"
    data = pd.read_csv(file)
    first_row = list(data.head(0))
    first_row.pop(0)
    first_row.pop(0)
    # print(first_row)
    for el in first_row:
        column=pd.to_numeric(data[el], errors='coerce')
        column.dropna(inplace=True)
        numeric_stats = {
        'mean': column.mean(),
        'median': column.median(),
        'mode': column.mode().iloc[0],  # Mode may have multiple values, so we take the first one
        'standard_deviation': column.std(),
        '25th_percentile': column.quantile(0.25),
        '75th_percentile': column.quantile(0.75),
        'minimum': column.min(),
        'maximum': column.max()
        }
        return numeric_stats
exam_analysis=dict()
for exam in individual_marks:
    if(exam!="total"):
        exam_analysis[exam]=ana(exam)

#getting grading analysis
# print(grade_boundaries)
# print(count)
def c_CPI(grade):
    if(grade=='AP' or grade=='AA'):
        return 10
    elif(grade=='AB'):
        return 9
    elif(grade=='BB'):
        return 8
    elif(grade=='BC'):
        return 7
    elif(grade=='CC'):
        return 6
    elif(grade=='CD'):
        return 5
    elif(grade=='DD'):
        return 4
    else:
        return "Failed"

###getting students attendance
ab=0
total=0
for exam in individual_marks:
    if(individual_marks[exam]=='a'):
        ab=ab+1
    total=total+1
ave_attend=100-ab*100/total

def upper_limit():
    ul=0
    for exam in exam_analysis:
        if(exam_analysis[exam]['maximum']>ul):
            ul=exam_analysis[exam]['maximum']
    return ul
######step 3: Make appropriate graphs
####graph 1: pie chart(subplots) attendance 
exams = list(data.head(0))
exams.pop(0)
exams.pop(0)
if(exams[-1]=="total"):
    exams.pop()
num_rows = len(exams)//2  # Number of rows
num_cols = len(exams)-num_rows  # Number of columns
num_subplots = num_rows * num_cols

fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 8)) # Create subplots

if num_subplots == 1: # Flatten the axs array if necessary
    axs = [[axs]]

for i, exam in enumerate(exams): # Iterate over exams and create pie charts for each subplot
    if i >= num_subplots:  # Check if all subplots are used
        break  # Exit the loop
    row = i // num_cols
    col = i % num_cols
    labels = ['Present', 'Absent']
    sizes = [len(data)-data[exam].eq('a').sum(), data[exam].eq('a').sum()]
    axs[row][col].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    axs[row][col].set_title(exam,fontweight='bold',fontsize=14)

for i in range(len(exams), num_subplots):
    row = i // num_cols
    col = i % num_cols
    axs[row][col].axis('off')

fig.suptitle('Attendance for Each Exam', fontsize=20, fontweight='bold')
plt.tight_layout()
# plt.show()
plt.savefig("attendance.png")

####graph 2: line graph of grades
grades = list(count.keys())
num_students = list(count.values())
fig, ax = plt.subplots()
plt.bar(grades, num_students, color='skyblue') #alpha for transparency/smudging effect
ax.set_xlabel('Grades',fontsize=14)
ax.set_ylabel('Number of Students',fontsize=14)
ax.set_title('Distribution of Grades',fontsize=18,fontweight='bold')
# plt.show()
plt.savefig("Grades_dist")

####graph 3: All exam line graphs with mean, maximum,student
new_data=dict()
for exam in individual_marks:
    if(exam!="total"):
        new_data[exam]={'Marks':individual_marks[exam],'Mean':exam_analysis[exam]['mean'],'Maximum':exam_analysis[exam]['maximum']}

x = []
marks = []
mean = []
max = []
for exam in new_data:
    x.append(exam)
    if(new_data[exam]['Marks']=='a'):
        marks.append(0)
    else:
        marks.append(float(new_data[exam]['Marks']))
    mean.append(new_data[exam]['Mean'])
    max.append(new_data[exam]['Maximum'])

plt.figure(figsize=(10,6))
plt.plot(x, marks, label='Student Marks')
plt.plot(x, mean, label='Mean', linestyle='--')
plt.plot(x, max, label='Maximum', linestyle='--')

# Add labels and legend
plt.xlabel('Exam Name',fontsize=14)
plt.ylabel('Marks',fontsize=14)
ul=upper_limit()
plt.ylim(0,ul*1.2)
plt.title('Performance Comparision',fontsize=14,fontweight='bold')
plt.legend()
# plt.show()
plt.savefig("compare")

######step 4: content in latex
"""
    1.) attendance of that student in exams(with congo, sad etc)
    2.) percentile, rank, grade, spi in overall exams
    3.) cutoff(tables) of grades
    4.) overall mean, highest,std dev

"""
over_str=""
hag_str=""
hag=0
for exam in individual_marks:
    if(exam!="total"):
        if(individual_marks[exam]=='a'):
            hag+=1
            hag_str+=" "+exam+"(absent)"
            continue
        if(float(individual_marks[exam])<float(exam_analysis[exam]['mean'])):
            hag+=1
            hag_str+=" "+exam
if(hag==0):
    over_str="Congratulations!You have been above average in all exams!"
elif(hag==len(individual_marks)-1 or hag==len(individual_marks)-2):
    over_str="Ahh! You have done extremely bad in "+hag_str
else:
    over_str="You have messed up in "+hag_str
# print(over_str)
if(ave_attend>90):
    att_remark='''Congratulations! Your attendance is '''+str(ave_attend)+'''\%'''
elif(ave_attend>70):
    att_remark="You have average attendance of "+str(ave_attend)+"\%"
elif(ave_attend>50):
    att_remark="You have been irregular in exams. Your attendance is "+str(ave_attend)+"\%"
else:
    att_remark="Your attendance is very less.Your attendance is "+str(ave_attend)+"\%"
att_remark=str(att_remark)
latex_template = r'''
\documentclass[a4paper, 11pt]{article}
\usepackage[top=3cm, bottom=3cm, left = 2cm, right = 2cm]{geometry} 
\geometry{a4paper} 
\usepackage[utf8]{inputenc}
\usepackage{textcomp}
\usepackage{graphicx} 
\usepackage{amsmath,amssymb}  
\usepackage{bm}  
\usepackage[pdftex,bookmarks,colorlinks,breaklinks]{hyperref}  
\usepackage{memhfixc} 
\usepackage{float}
\usepackage{pdfsync}  
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[R]{IIT BOMBAY}
\fancyhead[L]{\includegraphics[width=3cm]{IITB.png}}
\begin{document}
\definecolor{darkblue}{RGB}{0, 0, 139}
\begin{center}
    {\fontsize{30}{32}\selectfont \textbf{Performance Report}}
\end{center}
\vspace{2cm}
{\fontsize{16}{18}\selectfont \textbf{Name : \color{darkblue}''' + name + r'''}}\\ %name
\newline
{\fontsize{16}{18}\selectfont \textbf{Roll Number : \color{darkblue}'''+roll_no2+r'''}} %roll number
\vspace{1cm}
\section{\fontsize{20}{22}\textbf{Attendance}}
{\fontsize{14}{16}\textit{\underline{\color{darkblue}'''+ att_remark + r'''}}}\\ 
\vspace{1cm}
\section{\fontsize{20}{22}\textbf{Marks}}
\vspace{2cm}
\begin{table}[!h]
    \centering
    \fontsize{18}{20}\selectfont
    \begin{tabular}{|p{5cm}|p{5cm}|}
    \hline
    \textbf{Examination} & \textbf{Marks} \\
    \hline
    \hline\\'''
for key, value in individual_marks.items():
    latex_template += f"{key} & {value} \\\\\n"
    
latex_template+=r'''\hline
    \end{tabular}
\end{table}'''
latex_template+=r'''
\newpage
\vspace{3cm}
\section{\fontsize{20}{22}\textbf{Performance Index}}
\vspace{1cm}
{\fontsize{14}{16}\textit{\underline{Overall Grade : \color{darkblue}'''
latex_template+=Grade
latex_template+=r'''}}}\\
\newline
{\fontsize{14}{16}\textit{\underline{Current CPI : \color{darkblue}'''
latex_template+=str(c_CPI(Grade))
latex_template+=r'''}}}\\
\newline
{\fontsize{14}{16}\textit{\underline{Percentile : \color{darkblue}'''
latex_template+=str(percentile)
latex_template+=r'''}}}\\
\newline
{\fontsize{14}{16}\textit{\underline{Rank : \color{darkblue}'''
latex_template+=str(rank)
latex_template+=r'''}}}\\
\newline
{\fontsize{14}{14}\textbf{'''
latex_template+=over_str
latex_template+=r'''}}\\
\begin{figure}
    \centering
    \includegraphics[width=12cm,height=12cm]{compare.png}
    \caption{\textbf{Relative Analysis}}
\end{figure}
\vspace{2cm}
\begin{flushright}
    {\fontsize{22}{22}\textit{\textbf{\color{darkblue}Thank You}}}
\end{flushright}
\end{document}'''

# print (latex_template)

with open('result.tex', 'w') as f:
    f.write(latex_template)

