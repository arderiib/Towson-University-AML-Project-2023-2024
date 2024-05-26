#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:42:53 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

def raw_count(file_name):
    df = pd.read_csv(file_name)
    return df["raw_visitor_counts"].sum()

def calculate_visits_by_period(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = pd.Timestamp(start_year, start_month, start_day)
    end_date = pd.Timestamp(end_year, end_month, end_day)
    total_visits = 0

    for year in range(start_date.year, end_date.year + 1):
        for month in range(1, 13):
            if year == start_date.year and month < start_date.month:
                continue
            if year == end_date.year and month > end_date.month:
                continue
            name = f"/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_{year}_{month:0>2}.csv"
            try:
                total_visits += raw_count(name)
            except FileNotFoundError:
                print(f"File not found: {name}")

    return total_visits

# Define the time periods
periods = [
    {"start_year": 2019, "start_month": 1, "start_day": 1, "end_year": 2020, "end_month": 3, "end_day": 22},
    {"start_year": 2020, "start_month": 3, "start_day": 23, "end_year": 2021, "end_month": 7, "end_day": 1},
    {"start_year": 2021, "start_month": 7, "start_day": 1, "end_year": 2022, "end_month": 1, "end_day": 1}
]

# Calculate total visits for each period
period_visits = [calculate_visits_by_period(**period) for period in periods]

# Plot the data
plt.figure(figsize=(10, 6))
bars = plt.bar([f"{period['start_year']}-{period['end_year']}" for period in periods], period_visits)
plt.xlabel('Time Period')
plt.ylabel('Number of Raw Visitors')
plt.title('Number of Raw Visitors by Time Period')
plt.tight_layout()

# Add labels on top of each bar
for bar, count in zip(bars, period_visits):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, str(count), ha='center', va='bottom')

plt.show()