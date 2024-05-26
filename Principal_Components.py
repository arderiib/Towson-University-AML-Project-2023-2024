import pandas as pd
import math
import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def standardize(data):
    sum = 0
    for i in range(len(data)):
        sum = sum + data[i]
    mean = float(sum) / float(len(data))
    square_difference = 0
    for i in range(len(data)):
        square_difference = math.pow((data[i] - mean), 2) + square_difference
    variance = square_difference / float(len(data) - 1)
    standard_dev = math.sqrt(variance)
    for i in range(len(data)):
        data[i] = (data[i] - mean) / standard_dev
        
def covariance(data1, data2):
    cov = 0
    for i in range(len(data1)):
        cov = cov + (data1[i] * data2[i])
    cov = cov / float(len(data1) - 1)
    return cov



month = []
number_of_visits = []

print("Loading Mobility Data")
for i in range (2018,2023,1):
    for j in range (1,13,1):
        name = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_" + str(i) + "_" + str(f'{j:0>2.0f}' + ".csv")
        number_of_visits.append(counting(name))
        month.append(j)



print("Loading Crime Data")
FILE_NAME = "C:/Users/jonno/Towson University/Oleary, Michael - AML Criminology/Data Sources/Baltimore City Crime Data/Part_1_Crime_Data.csv"
df = pd.read_csv(FILE_NAME, low_memory=False)

YEAR_RANGE = [2018,2019,2020,2021,2022]
crime_count = [0] * 60

for i in range(len(df.loc[:,"CrimeDateTime"])):
    if int(df.loc[i,"CrimeDateTime"][0:4]) in YEAR_RANGE:
        crime_count[array_location(df.loc[i,"CrimeDateTime"])] = crime_count[array_location(df.loc[i,"CrimeDateTime"])] + 1
print("Finished Loading")
print("")
       
variables = [crime_count, number_of_visits, month]
variables_names = ["Crime Count", "Number of Visits", "Month"] 

for i in range(len(variables)):
    standardize(variables[i])

cov_matrix = np.array([[covariance(variables[i], variables[j]) for i in range(len(variables))] for j in range(len(variables))])

Eigenvalues , Eigenvectors = eig(cov_matrix)

Eigenvalues = Eigenvalues.tolist()
Eigenvectors = Eigenvectors.tolist()

sorted_Eigenvalues = sorted(Eigenvalues)
sorted_Eigenvectors = []

for i in range(len(Eigenvalues)):
    sorted_Eigenvectors.append(Eigenvectors[Eigenvalues.index(sorted_Eigenvalues[i])])

sum_of_eigenvalues = 0
for i in range(len(Eigenvalues)):
    sum_of_eigenvalues = sum_of_eigenvalues + Eigenvalues[i]
    
print("Each column represents data in this order...")
string = ""
for i in range(len(variables)):
    string = string + ", " + str(variables_names[i])
string = string[2:]
print("[" + string + "]")
print("")

for i in range(len(Eigenvalues)-1, -1, -1):
    print("PC" + str(len(Eigenvalues) - i) + " vector is...")
    print(sorted_Eigenvectors[i])
    print("with an eigenvalue of " + str(sorted_Eigenvalues[i]))
    print("which carries " + str((sorted_Eigenvalues[i]/sum_of_eigenvalues) * 100)[0:5] + "% of the variance of the data")
    print("")
    


