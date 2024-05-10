import pandas as pd
import sys
import os
from abs import grade_boundaries, count,mean_score,std_dev,high
mean_score=round(mean_score,2)
std_dev=round(std_dev,2)
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
data=pd.read_csv("main.csv")
data=list(data.head())
data.pop(0)
data.pop(0)
# print(data)
for exam in data:
    if(exam!="total"):
        exam_analysis[exam]=ana(exam)
for key1 in exam_analysis:
    for key2 in exam_analysis[key1]:
        exam_analysis[key1][key2]=round(exam_analysis[key1][key2],3)
# print(exam_analysis)
latex_template=r'''
\documentclass[a4paper, 11pt]{article}
\usepackage[top=3cm, bottom=3cm, left = 2cm, right = 2cm]{geometry} 
\geometry{a4paper} 
\usepackage[utf8]{inputenc}
\usepackage{textcomp}
\usepackage{graphicx} 
\usepackage{amsmath,amssymb}  
\usepackage{bm}  
\usepackage{float} 
\usepackage{dblfloatfix}
\usepackage[pdftex,bookmarks,colorlinks,breaklinks]{hyperref}  
\usepackage{memhfixc} 
\usepackage{pdfsync}  
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[R]{IIT BOMBAY}
\fancyhead[L]{\includegraphics[width=3cm]{IITB.png}}
\begin{document}
\definecolor{darkblue}{RGB}{0, 0, 139}
\begin{center}
    {\fontsize{30}{32}\selectfont \textbf{General Report}}
\end{center}
\vspace{2cm}
{\fontsize{16}{18}\selectfont \textbf{Overall Mean :\color{darkblue}'''
latex_template+=str(mean_score)
latex_template+=r''' }}\\ 
\newline
{\fontsize{16}{18}\selectfont \textbf{Overall Standard Deviation :\color{darkblue}'''
latex_template+=str(std_dev)
latex_template+=r''' }} \\%roll number
\newline
{\fontsize{16}{18}\selectfont \textbf{Overall Highest Score :\color{darkblue}'''
latex_template+=str(high)
latex_template+=r''' }}
\vspace{1cm}
\section{\fontsize{20}{22}\textbf{Attendance}}
{\fontsize{14}{16}\textit{\underline{The following pie chard predicts the same: }}}\\ %attendance line
\vspace{1cm}
\begin{figure}[H]
    \centering
    \includegraphics[width=18cm,height=12cm]{attendance.png}
\end{figure}
{\fontsize{2}{4}\selectfont \text{a}}\\
\vspace{3cm}\\
\newline
\newline\\\\
\newline
\section{\fontsize{20}{22}\textbf{Examination Statistics}}
\begin{table}[h]
    \centering
    \begin{tabular}{|p{2cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|p{1cm}|}
    \hline
    \textbf{Exams} & \textbf{Mean} & \textbf{Median} & \textbf{Mode} & \textbf{Std-Dev} & \textbf{25th \%} & \textbf{75th \%} & \textbf{Min} & \textbf{Max} \\
    \hline
    \hline\\'''
for key, value in exam_analysis.items():
    latex_template += f"{key} & {value['mean']} & {value['median']} & {value['mode']} & {value['standard_deviation']} & {value['25th_percentile']} & {value['75th_percentile']} & {value['minimum']} & {value['maximum']}\\\\\n"
latex_template+=r'''\hline
    \end{tabular}
\end{table}
\newpage
\vspace{7cm}
\section{\fontsize{20}{22}\textbf{Grading Statistics}}
\begin{table}[h]
    \centering
    \fontsize{14}{16}
    \begin{tabular}{|p{4cm}|p{4cm}|p{4cm}|}
    \hline
    \textbf{Grades} & \textbf{Number of Students} & \textbf{Cut-off score}\\
    \hline\\'''
for key, value in count.items():
    latex_template += f"{key} & {value} & {grade_boundaries[key]} \\\\\n"
latex_template+=r'''\hline
    \end{tabular}
\end{table}
\begin{figure}
    \centering
    \includegraphics[width=10cm,height=10cm]{Grades_dist.png}
    \caption{\textbf{Bell Shaped distribution}}
\end{figure}
\vspace{2cm}
\begin{flushright}
    {\fontsize{24}{26}\textit{\textbf{\color{darkblue}Thank You}}}
\end{flushright}
\end{document}
'''
with open('result.tex', 'w') as f:
    f.write(latex_template)