#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:26:56 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_day(df, crime_type):
    count = {day: 0 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    for i in range(len(df)):
        if df.loc[i, 'Description'] == crime_type:
            # Extract day of the week from the CrimeDateTime column
            day_of_week = df.loc[i, 'CrimeDateTime'].strftime('%A')
            # Increment the count for that day
            count[day_of_week] += 1
    return count

# List of unique crime types
crime_types = df['Description'].unique()

for crime_type in crime_types:
    crimes_by_day = count_crimes_by_day(df, crime_type)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.bar(crimes_by_day.keys(), crimes_by_day.values())
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of ' + crime_type + 's')
    plt.title('Number of ' + crime_type + 's by Day of the Week')

    # Add numbers on top of each bar
    for day, count in crimes_by_day.items():
        plt.text(day, count + 0.5, str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    print(crimes_by_day)