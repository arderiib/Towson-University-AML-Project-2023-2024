#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:15:39 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

def raw_count(file_name):
    df = pd.read_csv(file_name)
    return df["raw_visitor_counts"].sum()

def calculate_visits_by_season(name, months):
    total_visits = 0

    for year in range(2018, 2023):
        for month in months:
            file_name = f"/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_{year}_{month:0>2}.csv"
            try:
                total_visits += raw_count(file_name)
            except FileNotFoundError:
                print(f"File not found: {file_name}")

    return total_visits

# Define the seasons
seasons = [
    {"name": "Winter", "months": [1, 2, 12]},  # Winter
    {"name": "Spring", "months": [3, 4, 5]},   # Spring
    {"name": "Summer", "months": [6, 7, 8]},   # Summer
    {"name": "Fall", "months": [9, 10, 11]}    # Fall
]

# Calculate total visits for each season
season_visits = [calculate_visits_by_season(**season) for season in seasons]

# Plot the data
plt.figure(figsize=(10, 6))
bars = plt.bar(['Winter', 'Spring', 'Summer', 'Fall'], season_visits)
plt.xlabel('Season')
plt.ylabel('Number of Raw Visitors')
plt.title('Number of Raw Visitors by Season')
plt.tight_layout()

# Add labels on top of each bar
for bar, count in zip(bars, season_visits):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, str(count), ha='center', va='bottom')

plt.show()



