import sys
import pandas as pd
import os

def ana(file):
    # file=sys.argv[1]
    file_extension = os.path.splitext(file)[1]
    if(file_extension!=".csv"):
        file=file+".csv"
    data = pd.read_csv(file)
    first_row = list(data.head(0))
    first_row.pop(0)
    first_row.pop(0)
    # print(first_row)
    for el in first_row:
        print("======",el,"======")
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
        for key, values in numeric_stats.items():
            print(f"{key.capitalize()}:")
            print(values)
            print()

if __name__ == "__main__":
 
    # Print statistics for each numeric column
    bool=input("Do you want statistics for all exams or for a particular one?(1/2)")
    if(bool=='1'):
        data=ana("main.csv")
    elif(bool=='2'):
        file=str(input("Enter Exam name: "))
        data=ana(file)
    else:
        print("Wrong command!")
