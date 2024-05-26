#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:44:21 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd
import json

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_day(df):
    count = {day: 0 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    for i in range(len(df)):
        # Extract day of the week from the CrimeDateTime column
        day_of_week = df.loc[i, 'CrimeDateTime'].strftime('%A')
        # Increment the count for that day
        count[day_of_week] += 1
    return count

crimes_by_day = count_crimes_by_day(df)

# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(crimes_by_day.keys(), crimes_by_day.values())
plt.xlabel('Day of the Week')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes by Day of the Week')
plt.tight_layout()
plt.show()

print(crimes_by_day)