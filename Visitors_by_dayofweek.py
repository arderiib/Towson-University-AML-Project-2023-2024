#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:31:24 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd
import json

def raw_count(file_name):
    df = pd.read_csv(file_name)
    count = {}
    for i in range(len(df)):
        # Convert the string in 'popularity_by_day' to a dictionary
        popularity_by_day = json.loads(df.loc[i, "popularity_by_day"].replace("'", "\""))
        # Sum the counts for each day
        for day, value in popularity_by_day.items():
            count[day] = count.get(day, 0) + value
    return count

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
number_of_visits = {day: 0 for day in days_of_week}

for i in range(2018, 2023):
    for j in range(1, 13):
        name = f"/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_{i}_{j:0>2}.csv"
        counts = raw_count(name)
        for day, value in counts.items():
            number_of_visits[day] += value

# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(number_of_visits.keys(), number_of_visits.values())
plt.xlabel('Day of the Week')
plt.ylabel('Number of Raw Visitors')
plt.title('Number of Raw Visitors by Day of the Week')
plt.tight_layout()
plt.show()