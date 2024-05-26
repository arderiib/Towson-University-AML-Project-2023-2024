#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 00:44:44 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_period(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = pd.Timestamp(start_year, start_month, start_day)
    end_date = pd.Timestamp(end_year, end_month, end_day)
    total_crimes = df[(df['CrimeDateTime'].dt.tz_localize(None) >= start_date) & (df['CrimeDateTime'].dt.tz_localize(None) <= end_date)].shape[0]
    return total_crimes

# Define the time periods
periods = [
    {"start_year": 2018, "start_month": 1, "start_day": 1, "end_year": 2018, "end_month": 12, "end_day": 31},
    {"start_year": 2019, "start_month": 1, "start_day": 1, "end_year": 2019, "end_month": 12, "end_day": 31},
    {"start_year": 2020, "start_month": 1, "start_day": 1, "end_year": 2020, "end_month": 12, "end_day": 31},
    {"start_year": 2021, "start_month": 1, "start_day": 1, "end_year": 2021, "end_month": 12, "end_day": 31},
    {"start_year": 2022, "start_month": 1, "start_day": 1, "end_year": 2022, "end_month": 12, "end_day": 31}
]

# Calculate total crimes for each period
period_crimes = [count_crimes_by_period(**period) for period in periods]

# Plot the data
plt.figure(figsize=(10, 6))
bars = plt.bar([f"{period['start_year']}" for period in periods], period_crimes)
plt.xlabel('Time Period')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes by Year')
plt.tight_layout()

# Add labels on top of each bar
for bar, count in zip(bars, period_crimes):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(count), ha='center', va='bottom')

plt.show()