#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:08:37 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def raw_count(file_name):
    df = pd.read_csv(file_name)
    return df["raw_visitor_counts"].sum()

number_of_visits = []
years = []

for i in range(2018, 2023):
    year_total = 0
    for j in range(1, 13):
        name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Mobility Data/Automated Downloads/Baltimore_" + str(i) + "_" + str(f'{j:0>2.0f}' + ".csv")
        try:
            year_total += raw_count(name)
        except FileNotFoundError:
            print(f"File not found: {name}")
    number_of_visits.append(year_total)
    years.append(i)

file_name = "/Users/kiraparsons/Library/CloudStorage/OneDrive-TowsonUniversity/AML Criminology/Data Sources/Baltimore City Crime Data/Cleaned_Crime_Data2.Feb7.csv"

df = pd.read_csv(file_name)
df['CrimeDateTime'] = pd.to_datetime(df['CrimeDateTime'])

# Filter the DataFrame to include data from 2018 onwards
df = df[df['CrimeDateTime'].dt.year >= 2018]

# Extract year to group the data
df['Year'] = df['CrimeDateTime'].dt.year

# Group by year and count the number of crimes
yearly_counts = df.groupby('Year').size().reset_index(name='Count')

# Plot the data
fig, ax1 = plt.subplots(figsize=(12, 6))

bar_width = 0.35
index = np.arange(len(years))

# Bar plot for crimes
bars1 = ax1.bar(index, yearly_counts['Count'], bar_width, color='b', label='Crimes')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Crimes', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a second y-axis for visits
ax2 = ax1.twinx()
bars2 = ax2.bar(index + bar_width, number_of_visits, bar_width, color='r', alpha=0.5, label='Visits')
ax2.set_ylabel('Number of Raw Visitors', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Combine legend for both plots
bars = bars1 + bars2
labels = [bar.get_label() for bar in bars]
plt.legend(bars, labels, loc='upper left')

plt.xticks(index + bar_width / 2, years)
plt.title('Number of Crimes and Raw Visitors per Year')
plt.tight_layout()
plt.show()

