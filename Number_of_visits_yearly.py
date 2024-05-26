#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 23:23:32 2024

@author: kiraparsons
"""

import matplotlib.pyplot as plt
import pandas as pd

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

plt.figure(figsize=(10, 6))
bars = plt.bar(years, number_of_visits)
plt.xlabel('Year')
plt.ylabel('Number of Raw Visitors')
plt.title('Number of Raw Visitors Per Year')
plt.xticks(years)
plt.tight_layout()

for bar, count in zip(bars, number_of_visits):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100, str(count), ha='center', va='bottom')

plt.show()