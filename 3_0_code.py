# -*- coding: utf-8 -*-
"""3.0 Code

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mDX1vYLT56SHt1ZkE5p_ZnX563X8Anb0
"""

import gdown
import geopandas as gpd
import pandas as pd

def download_geospatial_data():
    # Download Crime Data
    crime_id = "1BrYiU8Y7l9WwPPDUdrahendeDAInbAhV"
    crime_url = f'https://drive.google.com/uc?id={crime_id}&export=download'
    crime_file = "Cleaned_Crime_Data2.xlsx"
    gdown.download(crime_url, crime_file, quiet=True)
    #crime_df = pd.read_excel(crime_file, dtype={"Post": "string", "Ethnicity": "string"})
    # Specify the engine parameter as 'openpyxl' for Excel files
    crime_df = pd.read_excel(crime_file, dtype={"Post": "string", "Ethnicity": "string"}, engine='openpyxl')

    # Download Census Tract Data
    cencustract_id = "1wetNwizTYcsXSqyTbksisNu9i7BNPQbH"
    cencustract_url = f'https://drive.google.com/uc?id={cencustract_id}&export=download'
    md_tract_file = "cencustract.zip"
    gdown.download(cencustract_url, md_tract_file, quiet=True)
    md_tract = gpd.read_file(md_tract_file)

    # Download Census Block Group Data
    cencusbg_id = "1WepLNIJp6Y5Yz34BfdT5Mnhze5hepy9i"
    cencusbg_url = f'https://drive.google.com/uc?id={cencusbg_id}&export=download'
    md_bg_file = "cencusbg.zip"
    gdown.download(cencusbg_url, md_bg_file, quiet=True)
    md_bg = gpd.read_file(md_bg_file)

    # Download Baltimore Neighborhood Data
    balt_nbd_id = "1WYXznPtx-uThZe0_vkI_rsxAKGwucZua"
    balt_nbd_url = f'https://drive.google.com/uc?id={balt_nbd_id}&export=download'
    balt_nbd_file = "Neighborhood.zip"
    gdown.download(balt_nbd_url, balt_nbd_file, quiet=True)
    balt_nbd = gpd.read_file(balt_nbd_file)

    return {
        "crime_data": crime_df,
        "census_tract": md_tract,
        "census_block_group": md_bg,
        "baltimore_neighborhood": balt_nbd,
    }

def download_geospatial_data():
    # Download Crime Data
    crime_id = "1BrYiU8Y7l9WwPPDUdrahendeDAInbAhV"
    crime_url = f'https://drive.google.com/uc?id={crime_id}&export=download'
    crime_file = "Cleaned_Crime_Data1.xlsx"
    gdown.download(crime_url, crime_file, quiet=True)
    crime_df = pd.read_excel(crime_file, dtype={"Post": "string", "Ethnicity": "string"})

    # Download Census Tract Data
    cencustract_id = "1wetNwizTYcsXSqyTbksisNu9i7BNPQbH"
    cencustract_url = f'https://drive.google.com/uc?id={cencustract_id}&export=download'
    md_tract_file = "cencustract.zip"
    gdown.download(cencustract_url, md_tract_file, quiet=True)
    md_tract = gpd.read_file(md_tract_file)

    # Download Census Block Group Data
    cencusbg_id = "1WepLNIJp6Y5Yz34BfdT5Mnhze5hepy9i"
    cencusbg_url = f'https://drive.google.com/uc?id={cencusbg_id}&export=download'
    md_bg_file = "cencusbg.zip"
    gdown.download(cencusbg_url, md_bg_file, quiet=True)
    md_bg = gpd.read_file(md_bg_file)

    # Download Baltimore Neighborhood Data
    balt_nbd_id = "1WYXznPtx-uThZe0_vkI_rsxAKGwucZua"
    balt_nbd_url = f'https://drive.google.com/uc?id={balt_nbd_id}&export=download'
    balt_nbd_file = "Neighborhood.zip"
    gdown.download(balt_nbd_url, balt_nbd_file, quiet=True)
    balt_nbd = gpd.read_file(balt_nbd_file)

    return {
        "crime_data": crime_df,
        "census_tract": md_tract,
        "census_block_group": md_bg,
        "baltimore_neighborhood": balt_nbd,
    }

data = download_geospatial_data()
crime_df = data["crime_data"]
md_tract = data["census_tract"]
md_bg = data["census_block_group"]
balt_nbd = data["baltimore_neighborhood"]

from google.colab import output
output.enable_custom_widget_manager()

balt_tract = md_tract.loc[md_tract['COUNTYFP'] == '510']

crime_san_df = crime_df
crime_san_gdf = gpd.GeoDataFrame(crime_san_df,
                                geometry=gpd.points_from_xy(crime_san_df.Longitude,
                                                            crime_san_df.Latitude),
                                crs="EPSG:4326")
#crime_san_gdf.head()

tract_join = gpd.sjoin(balt_tract.to_crs('EPSG:4269'),crime_san_gdf.to_crs('EPSG:4269'))
#tract_join.head()

# Commented out IPython magic to ensure Python compatibility.
!pip install ipympl
!pip install contextily
!pip install pointpats
!pip install mapclassify
!pip install pysal
# %matplotlib widget
import pandas as pd
import numpy as np
import geopandas as gpd
import datetime
import shapely
import contextily as ctx

tract_pivot = pd.pivot_table(tract_join,index='GEOID', columns='Description',
                             aggfunc={'Description':len})
#tract_pivot.head()

tract_pivot.columns = tract_pivot.columns.droplevel()
tract_crime = balt_tract.to_crs('EPSG:4269').merge(tract_pivot, how='left', on="GEOID")
#tract_crime.head()

nbd_join = gpd.sjoin(balt_nbd.to_crs('EPSG:4269'),crime_san_gdf.to_crs('EPSG:4269'))
#nbd_join.head()

nbd_pivot = pd.pivot_table(nbd_join,index='OBJECTID', columns='Description',
                           aggfunc={'Description':len})
#nbd_pivot.head()

nbd_pivot.columns = nbd_pivot.columns.droplevel()
nbd_crime = balt_nbd.to_crs('EPSG:4269').merge(nbd_pivot, how='left', on="OBJECTID")
#nbd_crime.head()

from google.colab import output
output.enable_custom_widget_manager()

from pointpats import PointPattern
import matplotlib.pyplot as plt

# Filter the Census Tract 1703
cen_tract = "1703"
tract_num = balt_tract[balt_tract['NAME'] == cen_tract]

# Calculate the bounding box based on the geometry of Census Tract 1703
min_x, min_y, max_x, max_y = tract_num.total_bounds

# Calculate the number of rows and columns
rows, cols = 4, 4

# Calculate the width and height of each subsection
width = (max_x - min_x) / cols
height = (max_y - min_y) / rows

# Create an empty list to store subsection geometries
subsections = []

# Generate the subsections
for row in range(rows):
    for col in range(cols):
        left = min_x + col * width
        right = left + width
        top = max_y - row * height
        bottom = top - height
        subsection = shapely.geometry.box(left, bottom, right, top)
        subsections.append(subsection)

# Create a GeoDataFrame for the subsections
subsections_gdf = gpd.GeoDataFrame({'geometry': subsections}, crs=tract_num.crs)

# Plot the bounding box
bounding_box_gdf = gpd.GeoDataFrame({'geometry': [shapely.geometry.box(min_x, min_y, max_x, max_y)], 'name': ['Bounding Box']}, crs=tract_num.crs)
bounding_box_gdf.plot(color='red', edgecolor='black', linewidth=1)

# Plot Census Tract 1703 on top of the bounding box
tract_num.plot(ax=plt.gca(), facecolor='none', edgecolor='green', linewidth=2)

# Plot the subsections
subsections_gdf.plot(ax=plt.gca(), color='none', edgecolor='blue', linewidth=1)

# Set the plot limits to match the bounding box coordinates
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)

plt.show()

# Ensure that both datasets have the same CRS
crime_san_gdf = crime_san_gdf.to_crs(tract_num.crs)

# Perform the spatial join to find crimes within Census Tract 1703
crimes_in_tract = gpd.sjoin(crime_san_gdf, tract_num, predicate="within")

# Count the number of crimes within Census Tract 1703
total_crimes_in_tract = len(crimes_in_tract)

print(f"Total number of crimes in Census Tract 1703: {total_crimes_in_tract}")

import geopandas as gpd
import libpysal as ps
import numpy as np
from pointpats import PointPattern, PoissonPointProcess
import pointpats.quadrat_statistics as qs
import matplotlib.pyplot as plt

# Create a PointPattern object with crime locations
crime_points = np.array([point.xy for point in crimes_in_tract.geometry])
crime_points_flat = crime_points.reshape(-1, 2)  # Flatten the array

pp_crime = PointPattern(crime_points_flat)

# Add crime count as an attribute to the PointPattern object
pp_crime.crime_count = np.ones(len(crime_points_flat))

# Display summary information for crime point pattern
pp_crime.summary()
pp_crime.plot(window=True, title="Crime Point Pattern")

# Rectangle quadrats & analytical sampling distribution
q_r = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4)
q_r.plot()
print(f"Chi-squared test statistic: {q_r.chi2}")
print(f"Degrees of freedom: {q_r.df}")
print(f"Analytical p-value: {q_r.chi2_pvalue}")

# Rectangle quadrats & empirical sampling distribution
csr_process = PoissonPointProcess(pp_crime.window, pp_crime.n, 999, asPP=True)
q_r_e = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4, realizations=csr_process)
print(f"Empirical p-value: {q_r_e.chi2_r_pvalue}")

!pip install libpysal
!pip install pointpats

# Ensure that both datasets have the same CRS
crime_san_gdf = crime_san_gdf.to_crs(tract_num.crs)

# Perform the spatial join to find crimes within Census Tract 1703
crimes_in_tract = gpd.sjoin(crime_san_gdf, tract_num, predicate="within")

# Count the number of agg assult crimes in 2015 in Census tract 1703
filtered_crimes = crimes_in_tract[(crimes_in_tract['Description'] == 'ARSON') &
                                  (crimes_in_tract['CrimeDateTime'] >= '2015/01/01') &
                                  (crimes_in_tract['CrimeDateTime'] < '2016/01/01')]
total = len(filtered_crimes)

# Count the number of crimes within Census Tract 1703
total_crimes_in_tract = len(crimes_in_tract)

print(f"Total number of crimes in Census Tract 1703: {total_crimes_in_tract}")
print(f'Total number of ARSON in 2015 in Census Tract 1703: {total}')

import geopandas as gpd
from shapely.geometry import Point
from pointpats import PointPattern, PoissonPointProcess, quadrat_statistics as qs
import matplotlib.pyplot as plt
import pandas as pd
from google.colab import drive
drive.mount('/content/drive')

# List of crime descriptions to loop through
crime_descriptions = ['AGG. ASSAULT', 'ARSON', 'AUTO THEFT', 'BURGLARY', 'COMMON ASSAULT',
                      'HOMICIDE', 'LARCENY FROM AUTO', 'LARCENY', 'RAPE', 'ROBBERY - CARJACKING',
                      'ROBBERY - COMMERCIAL', 'ROBBERY', 'SHOOTING']

for crime_description in crime_descriptions:
    filtered_crimes = crimes_in_tract[(crimes_in_tract['Description'] == crime_description) &
                                      (crimes_in_tract['CrimeDateTime'] >= '2015/01/01') &
                                      (crimes_in_tract['CrimeDateTime'] < '2016/01/01')]

    # Check for NaN values in the crime data
    if filtered_crimes.isnull().values.any():
        print(f"Skipping {crime_description} due to NaN values in the data.")
        continue

    # Remove rows with NaN values
    filtered_crimes = filtered_crimes.dropna(subset=['Longitude', 'Latitude'])

    # Check for NaN values after dropping
    if filtered_crimes.isnull().values.any():
        print(f"Skipping {crime_description} due to NaN values after dropping.")
        continue

    # Create a GeoDataFrame with the filtered crime data
    geometry = [Point(xy) for xy in zip(filtered_crimes['Longitude'], filtered_crimes['Latitude'])]
    filtered_gdf = gpd.GeoDataFrame(filtered_crimes, geometry=geometry, crs=crimes_in_tract.crs)

    # Extract x and y coordinates from the 'geometry' column
    crime_points = np.array([point.xy for point in filtered_gdf['geometry']])
    crime_points_flat = crime_points.reshape(-1, 2)

    # Create a PointPattern object with the filtered crime locations
    pp_crime = PointPattern(crime_points_flat)

    # Add crime count as an attribute to the PointPattern object
    pp_crime.crime_count = np.ones(len(crime_points_flat))

    # Display summary information for the crime point pattern
    pp_crime.summary()
    pp_crime.plot(window=True, title=f"Crime Point Pattern - {crime_description}")

    # Rectangle quadrats & analytical sampling distribution
    try:
        if pp_crime.window.get_area() < 1e-10:  # Skip if the window area is close to zero
            print(f"Skipping analytical sampling distribution for {crime_description} due to small window area.")
        else:
            q_r = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4)
            q_r.plot()
            print(f"Chi-squared test statistic: {q_r.chi2}")
            print(f"Degrees of freedom: {q_r.df}")
            print(f"Analytical p-value: {q_r.chi2_pvalue}")
    except Exception as e:
        print(f"Error in analytical sampling distribution: {e}")

    # Rectangle quadrats & empirical sampling distribution
    try:
        if pp_crime.window.get_area() < 1e-10:  # Skip if the window area is close to zero
            print(f"Skipping empirical sampling distribution for {crime_description} due to small window area.")
        else:
            csr_process = PoissonPointProcess(pp_crime.window, pp_crime.n, 999, asPP=True)
            q_r_e = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4, realizations=csr_process)
            print(f"Empirical p-value: {q_r_e.chi2_r_pvalue}")
    except Exception as e:
        print(f"Error in empirical sampling distribution: {e}")

    # Add a separator line between different crime descriptions for better readability
    print('-' * 40)

    # Create a DataFrame with summary information
    summary_data = {
       'Type of Crime': [crime_descriptions],
       'Year' : ['2015'],
       'Number of points': [len(pp_crime.points)],
       'Chi-squared test': [q_r.chi2],
       'Analytical p-value': [q_r.chi2_pvalue],
        # Add more relevant statistics as needed
    }

    df = pd.DataFrame(summary_data)

    df.to_csv('/content/drive/My Drive/data.csv', index=False)

    plt.show()

# Create a GeoDataFrame with the filtered crime data
#geometry = [Point(xy) for xy in zip(filtered_crimes['Longitude'], filtered_crimes['Latitude'])]
#filtered_gdf = gpd.GeoDataFrame(filtered_crimes, geometry=geometry, crs=crimes_in_tract.crs)

# Extract x and y coordinates from the 'geometry' column
#crime_points = np.array([point.xy for point in filtered_gdf['geometry']])
#crime_points_flat = crime_points.reshape(-1, 2)

# Create a PointPattern object with the filtered crime locations
#pp_crime = PointPattern(crime_points_flat)

# Add crime count as an attribute to the PointPattern object
#pp_crime.crime_count = np.ones(len(crime_points_flat))

# Extract the bounding box of the window
#minx, miny, maxx, maxy = pp_crime.window.bbox

# Calculate the area of the window
#window_area = (maxx - minx) * (maxy - miny)

# Plot the crime point pattern
#pp_crime.plot(window=True, title="Crime Point Pattern")

# Rectangle quadrats & analytical sampling distribution
#q_r = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4)
#q_r.plot()
#print(f"Chi-squared test statistic: {q_r.chi2}")
#print(f"Degrees of freedom: {q_r.df}")
#print(f"Analytical p-value: {q_r.chi2_pvalue}")

# Rectangle quadrats & empirical sampling distribution
#csr_process = PoissonPointProcess(pp_crime.window, pp_crime.n, 999, asPP=True)
#q_r_e = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4, realizations=csr_process)
#print(f"Empirical p-value: {q_r_e.chi2_r_pvalue}")

# Create a DataFrame with summary information
#summary_data = {
    #'Type of Crime': [crime_descriptions],
   # 'Year' : ['2015'],
   #'Number of points': [len(pp_crime.points)],
    #'Chi-squared test': [q_r.chi2],
   # 'Analytical p-value': [q_r.chi2_pvalue],
    # Add more relevant statistics as needed
#}

#df = pd.DataFrame(summary_data)

#df.to_csv('/content/drive/My Drive/mydata.csv', index=False)

#plt.show()

import geopandas as gpd
from shapely.geometry import Point
from pointpats import PointPattern, PoissonPointProcess, quadrat_statistics as qs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from google.colab import drive

drive.mount('/content/drive')

# List of crime descriptions to loop through
crime_descriptions = ['AGG. ASSAULT', 'ARSON', 'AUTO THEFT', 'BURGLARY', 'COMMON ASSAULT',
                      'HOMICIDE', 'LARCENY FROM AUTO', 'LARCENY', 'RAPE', 'ROBBERY - CARJACKING',
                      'ROBBERY - COMMERCIAL', 'ROBBERY', 'SHOOTING']

# Create an empty DataFrame to store summary information
summary_data_list = []

# Loop through each crime description
for crime_description in crime_descriptions:
    # Filter crimes based on crime description and date range
    filtered_crimes = crimes_in_tract[(crimes_in_tract['Description'] == crime_description) &
                                      (crimes_in_tract['CrimeDateTime'] >= '2015/01/01') &
                                      (crimes_in_tract['CrimeDateTime'] < '2016/01/01')]

    # Check for NaN values in the crime data
    if filtered_crimes.isnull().values.any():
        print(f"Skipping {crime_description} due to NaN values in the data.")
        continue

    # Remove rows with NaN values
    filtered_crimes = filtered_crimes.dropna(subset=['Longitude', 'Latitude'])

    # Check for NaN values after dropping
    if filtered_crimes.isnull().values.any():
        print(f"Skipping {crime_description} due to NaN values after dropping.")
        continue

    # Create a GeoDataFrame with the filtered crime data
    geometry = [Point(xy) for xy in zip(filtered_crimes['Longitude'], filtered_crimes['Latitude'])]
    filtered_gdf = gpd.GeoDataFrame(filtered_crimes, geometry=geometry, crs=crimes_in_tract.crs)

    # Extract x and y coordinates from the 'geometry' column
    crime_points = np.array([point.xy for point in filtered_gdf['geometry']])
    crime_points_flat = crime_points.reshape(-1, 2)

    # Create a PointPattern object with the filtered crime locations
    pp_crime = PointPattern(crime_points_flat)

    # Add crime count as an attribute to the PointPattern object
    pp_crime.crime_count = np.ones(len(crime_points_flat))

    # Display summary information for the crime point pattern
    pp_crime.summary()
    pp_crime.plot(window=True, title=f"Crime Point Pattern - {crime_description}")

     # Initialize q_r and q_r_e variables
    q_r, q_r_e = None, None

    # Rectangle quadrats & analytical sampling distribution
    try:
        if pp_crime.window.area < 1e-10:
            print(f"Skipping analytical sampling distribution for {crime_description} due to small window area.")
        else:
            q_r = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4)
            q_r.plot()
            print(f"Chi-squared test statistic: {q_r.chi2}")
            print(f"Degrees of freedom: {q_r.df}")
            print(f"Analytical p-value: {q_r.chi2_pvalue}")
    except Exception as e:
        print(f"Error in analytical sampling distribution: {e}")

    # Rectangle quadrats & empirical sampling distribution
    try:
        if pp_crime.window.area < 1e-10:
            print(f"Skipping empirical sampling distribution for {crime_description} due to small window area.")
        else:
            csr_process = PoissonPointProcess(pp_crime.window, pp_crime.n, 999, asPP=True)
            q_r_e = qs.QStatistic(pp_crime, shape="rectangle", nx=4, ny=4, realizations=csr_process)
            print(f"Empirical p-value: {q_r_e.chi2_r_pvalue}")
    except Exception as e:
        print(f"Error in empirical sampling distribution: {e}")

    # Add a separator line between different crime descriptions for better readability
    print('-' * 40)

    # Append summary information to the list
    summary_data_list.append({
        'Type of Crime': crime_description,
        'Year': '2015',
        'Number of points': len(pp_crime.points),
        'Chi-squared test': q_r.chi2 if q_r else np.nan,
        'Analytical p-value': q_r.chi2_pvalue if q_r else np.nan,
        'Empirical p-value': q_r_e.chi2_r_pvalue if q_r_e else np.nan,
    })

    plt.show()

# Create a DataFrame with summary information
summary_df = pd.DataFrame(summary_data_list)

# Export summary information to CSV
summary_df.to_csv('/content/drive/My Drive/mydata.csv', index=False)

from IPython.display import IFrame
import folium

# Define the center of the map
center_lat, center_lon = 39.2904, -76.6122

# Create a Folium Map object
m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# Plotting each neighborhood polygon on the map
for idx, row in balt_nbd.iterrows():
    folium.GeoJson(row.geometry).add_to(m)

# Save the map to an HTML file
m.save("baltimore_neighborhoods_map.html")

# Display the map inline in the notebook
IFrame(src='baltimore_neighborhoods_map.html', width=700, height=600)