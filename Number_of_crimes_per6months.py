#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 22:42:24 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

# Extract month and year to group the data
df['Month'] = df['CrimeDateTime'].dt.month
df['Year'] = df['CrimeDateTime'].dt.year

# Group by month and year and count the number of crimes
monthly_counts = df.groupby(['Year', 'Month']).size().reset_index(name='Count')

# Create a list of month-year labels for plotting, updated every 6 months
time = [f"{row['Year']}-{row['Month']}" for index, row in monthly_counts.iterrows() if row['Month'] % 6 == 0]

# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(range(len(monthly_counts)), monthly_counts['Count'])
plt.xlabel('Month-Year')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes per Month-Year')
plt.xticks(range(0, len(monthly_counts), 6), time, rotation=45)
plt.tight_layout()
plt.show() 
        
print(monthly_counts)