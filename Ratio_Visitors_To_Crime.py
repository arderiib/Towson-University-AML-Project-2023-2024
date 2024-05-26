#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:34:18 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

def raw_count(file_name):
    df = pd.read_csv(file_name)
    return df["raw_visitor_counts"].sum()

def calculate_count(file_name, is_visits, months):
    if is_visits:
        total_count = 0
        for year in range(2018, 2023):
            for month in months:
                file_path = file_name.format(year, month)
                try:
                    total_count += raw_count(file_path)
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
        return total_count
    else:
        df = pd.read_csv(file_name)
        df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])
        total_crimes = df[df['CrimeDateTime'].dt.month.isin(months)].shape[0]
        return total_crimes

# Define the file path templates
visits_file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_{0}_{1:0>2}.csv"
crimes_file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

# Define the seasons
seasons = [
    {"name": "Winter", "months": [1, 2, 12]},  # Winter
    {"name": "Spring", "months": [3, 4, 5]},   # Spring
    {"name": "Summer", "months": [6, 7, 8]},   # Summer
    {"name": "Fall", "months": [9, 10, 11]}    # Fall
]

# Calculate total counts for each season
season_counts_visits = [calculate_count(visits_file_name, True, season["months"]) for season in seasons]
season_counts_crimes = [calculate_count(crimes_file_name, False, season["months"]) for season in seasons]

# Plot the data side by side
plt.figure(figsize=(15, 8))

bar_width = 0.35
index = range(len(seasons))

bars_visits = plt.bar(index, season_counts_visits, bar_width, label='Visitors', color='b')
bars_crimes = plt.bar([i + bar_width for i in index], season_counts_crimes, bar_width, label='Crimes', color='r')

plt.xlabel('Season')
plt.ylabel('Counts')
plt.title('Number of Raw Visitors and Crimes by Season')
plt.xticks([i + bar_width / 2 for i in index], [season["name"] for season in seasons])
plt.legend()

# Add labels on top of each bar
for bar, count in zip(bars_visits, season_counts_visits):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, str(count), ha='center', va='bottom')

for bar, count in zip(bars_crimes, season_counts_crimes):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()


# Calculate the ratio of visitors to crimes for each season
ratio = [visits / crimes for visits, crimes in zip(season_counts_visits, season_counts_crimes)]

# Plot the data
plt.figure(figsize=(12, 6))
bars = plt.bar(['Winter', 'Spring', 'Summer', 'Fall'], ratio)
plt.xlabel('Season')
plt.ylabel('Ratio of Visitors to Crimes')
plt.title('Ratio of Visitors to Crimes by Season')
plt.tight_layout()

# Add labels on top of each bar
for bar, r in zip(bars, ratio):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{r:.2f}", ha='center', va='bottom')

plt.show()








