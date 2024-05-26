import matplotlib.pyplot as plt
import pandas as pd

def counting(file_name):
    df = pd.read_csv(file_name)
    count = 0
    for i in range(len(df.loc[:,"raw_visitor_counts"])):
        count = count + df.loc[i,"raw_visitor_counts"]
    return count

def array_location(date):
    year = int(date[0:4])
    month = int(date[5:7])
    return (year - 2018) * 12 + month - 1

time = []
number_of_visits = []

print("Loading Mobility Data")
for i in range (2018,2023,1):
    for j in range (1,13,1):
        name = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_" + str(i) + "_" + str(f'{j:0>2.0f}' + ".csv")
        number_of_visits.append(counting(name))

for i in range(len(number_of_visits)):
    time.append(i)

print("Loading Crime Data")
FILE_NAME = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Baltimore City Crime Data/Part_1_Crime_Data.csv"
df = pd.read_csv(FILE_NAME, low_memory=False)

YEAR_RANGE = [2018,2019,2020,2021,2022]
crime_count = [0] * 60
type_of_crime = crimes = ['AGG. ASSAULT', 'ARSON', 'AUTO THEFT','BURGLARY',
                  'COMMON ASSAULT','HOMICIDE', 'LARCENY',
                  'LARCENY FROM AUTO', 'RAPE', 'ROBBERY', 
                  'ROBBERY - CARJACKING', 'ROBBERY - COMMERCIAL',
                  'SHOOTING']

for j in range(len(type_of_crime)):
    print("Loading Graphs for " + str(type_of_crime[j]) + " Crime Type")
    for i in range(len(df.loc[:,"CrimeDateTime"])):
        if int(df.loc[i,"CrimeDateTime"][0:4]) in YEAR_RANGE and df.loc[i,"Description"] == type_of_crime[j]:
            crime_count[array_location(df.loc[i,"CrimeDateTime"])] = crime_count[array_location(df.loc[i,"CrimeDateTime"])] + 1
       
    
    plt.xlabel('Months starting from Jan 2018')
    plt.ylabel('Number of ' + str(type_of_crime[j]))
    plt.bar(time,crime_count)
    plt.show()

    plt.xlabel('Number of Raw Visitors')
    plt.ylabel('Number of ' + str(type_of_crime[j]))
    plt.plot(number_of_visits, crime_count, 'o')
    plt.show()
    
    plt.xlabel('Number of Raw Visitors')
    plt.ylabel('Number of ' + str(type_of_crime[j]))
    plt.plot(number_of_visits, crime_count)
    plt.show()
    
    crime_count = [0] * 60

print("Done :)")
