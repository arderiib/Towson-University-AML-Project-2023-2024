import matplotlib.pyplot as plt
import pandas as pd

def counting(file_name):
    df = pd.read_csv(file_name)
    count = 0
    for i in range(len(df.loc[:,"raw_visitor_counts"])):
        count = count + df.loc[i,"raw_visitor_counts"]
    return count

time = []
number_of_visits = []

for i in range (2018,2023,1):
    for j in range (1,13,1):
        name = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_" + str(i) + "_" + str(f'{j:0>2.0f}' + ".csv")
        number_of_visits.append(counting(name))

for i in range(len(number_of_visits)):
    time.append(i)
    
plt.xlabel('Months')
plt.ylabel('Number of Raw Visitors')
plt.bar(time,number_of_visits)

print(number_of_visits)