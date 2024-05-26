#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:18:43 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Part_1_Crime_Data.csv"
df = pd.read_csv(FILE_NAME)

YEAR_RANGE = [2018, 2019, 2020, 2021, 2022]  # Include 2022
crime_types = df['Description'].unique()

for crime_type in crime_types:
    print(f"Processing {crime_type} crimes")
    crime_count = {year: [0] * 12 for year in YEAR_RANGE}  # Initialize crime_count for each year
    for i in range(len(df)):
        crime_year = int(df.loc[i, "CrimeDateTime"][0:4])
        crime_month = int(df.loc[i, "CrimeDateTime"][5:7])
        if crime_year in YEAR_RANGE and df.loc[i, "Description"] == crime_type:
            crime_count[crime_year][crime_month - 1] += 1

    plt.figure()  # Create a new figure for each crime type
    plt.xlabel('Year')
    plt.ylabel(f'Number of {crime_type} Crimes')
    for idx, year in enumerate(YEAR_RANGE):
        x_values = [idx * 12 + month - 0.5 for month in range(1, 13)]  # Adjust x values to start from 0
        plt.bar(x_values, crime_count[year], label=str(year), color='mediumblue', alpha=0.7)  # Set bar color
    plt.title(f'Number of {crime_type} Crimes per Month')
    plt.xticks([(idx * 12)  for idx in range(len(YEAR_RANGE))], YEAR_RANGE)  # Show years on x-axis at the midpoint of each year
    plt.show()  # Show the current figure

# Show all figures at once
plt.show()