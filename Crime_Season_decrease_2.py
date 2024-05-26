#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 13:14:29 2024

@author: kiraparsons
"""

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

# Output percentage decrease in crime between winter and summer for each crime type
for crime_type in crime_types:
    season_crimes = [count_crimes_by_season_and_type(season["months"], crime_type) for season in seasons]
    winter_crimes = season_crimes[0]
    summer_crimes = season_crimes[2]
    decrease_percentage = ((winter_crimes - summer_crimes) / winter_crimes) * 100
    print(f'For {crime_type}: Winter-Summer Decrease: {decrease_percentage:.2f}%')
    print(f'Crimes in the summer: {summer_crimes}')
    print(f'Crimes in the winter: {winter_crimes}')