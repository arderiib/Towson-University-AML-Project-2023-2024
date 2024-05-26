#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:58:11 2024

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

def calculate_percentage_change(crimes_by_day):
    percentage_change = {}
    days = list(crimes_by_day.keys())
    for i in range(len(days) - 1):
        current_day = days[i]
        next_day = days[i + 1]
        current_count = crimes_by_day[current_day]
        next_count = crimes_by_day[next_day]
        change_percentage = ((next_count - current_count) / current_count) * 100
        percentage_change[f"{current_day} to {next_day}"] = change_percentage
    return percentage_change

# List of unique crime types
crime_types = df['Description'].unique()

for crime_type in crime_types:
    crimes_by_day = count_crimes_by_day(df, crime_type)
    percentage_change = calculate_percentage_change(crimes_by_day)

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

    print(f"Crime Type: {crime_type}")
    print("Percentage Change:")
    for period, change in percentage_change.items():
        print(f"{period}: {change:.2f}%")
        
        
        