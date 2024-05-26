# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E6X43F74aMP5yit5h-9_wPH2YTvxn9PO
"""

import gdown
import pandas as pd
import folium

# Download the crime data
url = 'https://drive.google.com/uc?id=1BrYiU8Y7l9WwPPDUdrahendeDAInbAhV'
output = 'crime_data.xlsx'
gdown.download(url, output, quiet=False)

# Load the crime data
crime_df = pd.read_excel(output, dtype={"Post": "string", "Ethnicity": "string"})

# Create a map centered on Baltimore
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12)

# Add crime data points to the map
for idx, row in crime_df.iterrows():
    folium.CircleMarker([row["Latitude"], row["Longitude"]], radius=3, color='red', fill=True, fill_color='red', fill_opacity=0.5).add_to(m)

# Display the map
m