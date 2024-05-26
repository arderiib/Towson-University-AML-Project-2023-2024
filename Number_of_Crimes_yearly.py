#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 23:15:31 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

# Extract year and month to group the data
df['Year'] = df['CrimeDateTime'].dt.year
df['Month'] = df['CrimeDateTime'].dt.month

# List of unique crime types
crime_types = df['Description'].unique()

# Plot for each crime type
for crime_type in crime_types:
    # Filter data for the current crime type
    crime_data = df[df['Description'] == crime_type]

    # Group by year and month and count the number of crimes
    monthly_counts = crime_data.groupby(['Year', 'Month']).size().reset_index(name='Count')

    # Filter the data to start from January 2018
    monthly_counts = monthly_counts[(monthly_counts['Year'] >= 2018)]

    # Plot the data
    plt.figure(figsize=(18, 6))
    bars = plt.bar(range(len(monthly_counts)), monthly_counts['Count'], color='skyblue')

    plt.xlabel('Year and Month')
    plt.ylabel(f'Number of {crime_type}')
    plt.title(f'Number of {crime_type} per Month')
    plt.xticks(range(len(monthly_counts)), [f'{year}-{month}' for year, month in zip(monthly_counts['Year'], monthly_counts['Month'])], rotation=45)
    plt.tight_layout()
    plt.show()





