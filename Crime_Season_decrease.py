#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:12:05 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

def count_crimes_by_season_and_type(months, crime_type):
    total_crimes = df[(df['CrimeDateTime'].dt.month.isin(months)) & (df['Description'] == crime_type)].shape[0]
    return total_crimes

# Define the seasons
seasons = [
    {"name": "Winter", "months": [1, 2, 12]},  # Winter
    {"name": "Spring", "months": [3, 4, 5]},   # Spring
    {"name": "Summer", "months": [6, 7, 8]},   # Summer
    {"name": "Fall", "months": [9, 10, 11]}    # Fall
]

# Define the crime types
crime_types = df['Description'].unique()

# Plot the data for each crime type separately
for crime_type in crime_types:
    plt.figure(figsize=(8, 6))
    season_crimes = [count_crimes_by_season_and_type(season["months"], crime_type) for season in seasons]
    
    # Calculate percentage decrease in crime between winter and summer
    winter_crimes = season_crimes[0]
    summer_crimes = season_crimes[2]
    decrease_percentage = ((winter_crimes - summer_crimes) / winter_crimes) * 100

    bars = plt.bar([season["name"] for season in seasons], season_crimes, alpha=0.7)

    # Add labels on top of each bar
    for bar, count in zip(bars, season_crimes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(count), ha='center', va='bottom')

    plt.xlabel('Season')
    plt.ylabel('Number of Crimes')
    plt.title(f'Number of {crime_type} by Season\nWinter-Summer Decrease: {decrease_percentage:.2f}%')
    plt.tight_layout()
    plt.show()