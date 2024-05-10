import pandas as pd
#step1: read csv file
data=pd.read_csv('main.csv')

#step2: calculate mean and std dev
mean_score = data['total'].mean()
std_dev = data['total'].std()
high=data['total'].max()

# Step 3: Define grade boundaries
grade_percentiles = [0, 0.05, 0.15,0.27, 0.4, 0.6 , 0.75, 0.88, 0.99]
grade_boundaries = {
    'AP': data['total'].quantile(grade_percentiles[8]),
    'AA': data['total'].quantile(grade_percentiles[7]),
    'AB': data['total'].quantile(grade_percentiles[6]),
    'BB': data['total'].quantile(grade_percentiles[5]),
    'BC': data['total'].quantile(grade_percentiles[4]),
    'CC': data['total'].quantile(grade_percentiles[3]),
    'CD': data['total'].quantile(grade_percentiles[2]),
    'DD': data['total'].quantile(grade_percentiles[1]),
    'F': data['total'].quantile(grade_percentiles[0])
}
# print(grade_boundaries)

count={
    'AP': 0,
    'AA': 0,
    'AB': 0,
    'BB': 0,
    'BC': 0,
    'CC': 0,
    'CD': 0,
    'DD': 0,
    'F': 0
}

# Step 4: Determine scores and assign grades
def assign_grade(score):
    # z_score = (score - mean_score) / std_dev
    
    if score >= grade_boundaries['AP']:
        count['AP']+=1
        return 'AP'
    elif score >= grade_boundaries['AA']:
        count['AA']+=1
        return 'AA'
    elif score >= grade_boundaries['AB']:
        count['AB']+=1
        return 'AB'
    elif score >= grade_boundaries['BB']:
        count['BB']+=1
        return 'BB'
    elif score >= grade_boundaries['BC']:
        count['BC']+=1
        return 'BC'
    elif score >= grade_boundaries['CC']:
        count['CC']+=1
        return 'CC'
    elif score >= grade_boundaries['CD']:
        count['CD']+=1
        return 'CD'
    elif score >= grade_boundaries['DD']:
        count['DD']+=1
        return 'DD'
    else:
        count['F']+=1
        return 'F'

data['Grade'] = data['total'].apply(assign_grade)
# print(count)
# Step 5: Print grades
selected_columns = ['Roll_Number','Name', 'Grade']
data[selected_columns].to_csv('grades.txt', sep=',', index=False)