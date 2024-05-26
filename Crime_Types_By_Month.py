#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:30:08 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd
import calendar

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_month(df, crime_type):
    count = {month: 0 for month in range(1, 13)}
    for i in range(len(df)):
        if df.loc[i, 'Description'] == crime_type:
            # Extract month from the CrimeDateTime column
            month = df.loc[i, 'CrimeDateTime'].month
            # Increment the count for that month
            count[month] += 1
    return count

# List of unique crime types
crime_types = df['Description'].unique()

for crime_type in crime_types:
    crimes_by_month = count_crimes_by_month(df, crime_type)

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.bar(crimes_by_month.keys(), crimes_by_month.values())
    plt.xlabel('Month')
    plt.ylabel('Number of ' + crime_type + 's')
    plt.title('Number of ' + crime_type + 's by Month')

    # Add numbers on top of each bar
    for month, count in crimes_by_month.items():
        plt.text(month, count + 0.5, str(count), ha='center', va='bottom')

    # Set month labels
    plt.xticks(range(1, 13), [calendar.month_name[i] for i in range(1, 13)])

    plt.tight_layout()
    plt.show()

    print(crimes_by_month)