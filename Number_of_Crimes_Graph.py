import matplotlib.pyplot as plt
import pandas as pd

def array_location(date):
    year = int(date[0:4])
    month = int(date[5:7])
    return (year - 2018) * 12 + month - 1

FILE_NAME = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Baltimore City Crime Data/Part_1_Crime_Data.csv"
df = pd.read_csv(FILE_NAME)

YEAR_RANGE = [2018,2019,2020,2021,2022]
crime_count = [0] * 12 * 5
time = []
for i in range(60):
    time.append(i)

for i in range(len(df.loc[:,"CrimeDateTime"])):
    if int(df.loc[i,"CrimeDateTime"][0:4]) in YEAR_RANGE:
        crime_count[array_location(df.loc[i,"CrimeDateTime"])] = crime_count[array_location(df.loc[i,"CrimeDateTime"])] + 1
        
plt.xlabel('Months')
plt.ylabel('Number of Crimes')
plt.bar(time,crime_count)

print(crime_count)