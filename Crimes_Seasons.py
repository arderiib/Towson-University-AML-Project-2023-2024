#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:08:05 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_season(months):
    total_crimes = df[df['CrimeDateTime'].dt.month.isin(months)].shape[0]
    return total_crimes

# Define the seasons
seasons = [
    {"name": "Winter", "months": [1, 2, 12]},  # Winter
    {"name": "Spring", "months": [3, 4, 5]},   # Spring
    {"name": "Summer", "months": [6, 7, 8]},   # Summer
    {"name": "Fall", "months": [9, 10, 11]}    # Fall
]

# Calculate total crimes for each season
season_crimes = [count_crimes_by_season(season["months"]) for season in seasons]

# Plot the data
plt.figure(figsize=(10, 6))
bars = plt.bar([season["name"] for season in seasons], season_crimes)
plt.xlabel('Season')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes by Season')
plt.tight_layout()

# Add labels on top of each bar
for bar, count in zip(bars, season_crimes):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(count), ha='center', va='bottom')

plt.show()