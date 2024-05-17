# -*- coding: utf-8 -*-
"""
Crime and Mobillity by Census Block Groups

Created on Tue Mar  5 10:08:24 2024

@author: moleary
"""
import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats.distributions import chi2
import shapely

import sys

# Set Crime File and Path Data
CWD = Path.cwd()

# Choose either the raw data or the cleaned data...

# Raw Crime Data
#CRIME_XLS = (CWD / "../../Data Sources/Baltimore City Crime Data" \
#                  "/Part_1_Crime_Data.xlsx")
#CRIME_XLS_SHEET_NAME = "Part_1_Crime_Data"  
#CRIME_PKL = (CWD / "Part_1_Crime_data.pkl")    

# Cleaned Crime Data 
CRIME_XLS = (CWD / "../../Data Sources/Baltimore City Crime Data" \
                  "/Cleaned_Crime_data1.xlsx")
CRIME_XLS_SHEET_NAME = "Sheet1"  
CRIME_PKL = (CWD / "Cleaned_Part_1_Crime_data.pkl") 

# Set Census File and Path Data
BLOCKGROUP_SHAPEFILE = (CWD / "../../Data Sources/Census/tl_2022_24_bg.zip")
TRACT_SHAPEFILE = (CWD / "../../Data Sources/Census/tl_2022_24_tract.zip")
BLOCK_SHAPEFILE = (CWD / "../../Data Sources/Census/tl_2022_24_tabblock20.zip")

# Census 2010 Data
BLOCKGROUP_2010_SHAPEFILE = \
       (CWD / "../../Data Sources/Census 2010/tl_2010_24_bg10.zip")

# Set Mobility Path
MOBILITY_DIR_PATH = (CWD / "../../Data Sources/Mobility Data" \
                            "/Automated Downloads")
MOBILITY_PKL =  (CWD / "Mobility.pkl")   

class crimes:
   def __init__(self,xls,sheetname,pkl):
      print("Loading Crime Data")
      if Path.exists(pkl):
         df = pd.read_pickle(pkl)
      else:
         df = pd.read_excel(io=xls, sheet_name=sheetname)
         print("Pickling Crime Data")
         pd.to_pickle(df,pkl)
      print("Crime Data Loaded")
      
      # Create Geodataframe. Assume EPSG 4326 for input
      geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
      temp_gdf = gpd.GeoDataFrame(df,
                                  geometry=geometry,
                                  crs = "EPSG:4326")
      
      # Store result as EPSG:3857 (which is how crimes are stored)
      self.gdf = temp_gdf.to_crs('EPSG:3857')
   
      # Coordinate Systems: 
      #   https://gis.stackexchange.com/questions/48949/epsg-3857-or-4326-for-web-mapping

   def mapplot(self,axis,crimetype=None):
      
      gdf = self.gdf
      if crimetype:
         gdf = self.gdf[self.gdf['Description'] == crimetype]
      
      gdf.plot(ax=axis,marker='o', markersize=0.25, color='blue')
           
class census2010:
   def __init__(self,shapefile):     
      mdgdf = gpd.read_file(shapefile)
      self.gdf = mdgdf.loc[mdgdf['COUNTYFP10'] == '510'].to_crs('EPSG:3857')
      self.gdf['area'] = self.gdf.to_crs('EPSG:6933')['geometry'].area /1E6
   
      # These are the fields in the initial data set
      # print(mdgdf.dtypes)
      # STATEFP10       object
      # COUNTYFP10      object
      # TRACTCE10       object
      # BLKGRPCE10      object
      # GEOID10         object
      # NAMELSAD10      object
      # MTFCC10         object
      # FUNCSTAT10      object
      # ALAND10          int64
      # AWATER10         int64
      # INTPTLAT10      object
      # INTPTLON10      object
      # geometry      geometry
      # dtype: object
      
      # Lets rewrite the names to match the 2020 data
      self.rename_columns()
      
      # Now the GEOID value is a Pandas object; we would like it 
      #  to be an integer
      self.gdf = self.gdf.astype({'GEOID':'UInt64'})
      
   def mapplot(self,axis):
      
      self.gdf.plot(ax=axis,edgecolor="red", facecolor="none", linewidth=1)
      

   def mapplot_geoid(self,axis,geoid):      
      df = self.gdf[self.gdf['GEOID'] == geoid]
      ax = df.plot(ax=axis,edgecolor="red", facecolor="none", linewidth=1, 
                         figsize=(10,10))

   def rename_columns(self):   
      self.gdf.rename(columns = {'STATEFP10':'STATEFP'}, inplace=True)
      self.gdf.rename(columns = {'COUNTYFP10':'COUNTYFP'}, inplace=True)
      self.gdf.rename(columns = {'TRACTCE10':'TRACTCE'}, inplace=True)
      self.gdf.rename(columns = {'BLOCKGRPCE10':'BLOCKCE'}, inplace=True)
      self.gdf.rename(columns = {'GEOID10':'GEOID'}, inplace=True)
      self.gdf.rename(columns = {'NAMELSAD10':'NAME'}, inplace=True)
      self.gdf.rename(columns = {'MTFCC10':'MTFCC'}, inplace=True)
      self.gdf.rename(columns = {'FUNCSTAT10':'FUNCSTAT'}, inplace=True)
      self.gdf.rename(columns = {'ALAND10':'ALAND'}, inplace=True)
      self.gdf.rename(columns = {'AWATER10':'AWATER'}, inplace=True)
      self.gdf.rename(columns = {'INTPTLAT10':'INTPTLAT'}, inplace=True)
      self.gdf.rename(columns = {'INTPTLON10':'INTPTLON'}, inplace=True)
   
class census:
   def __init__(self,shapefile):
   
      mdgdf = gpd.read_file(shapefile)
      
      # The Census Block level data uses slightly different column names. 
      # Adjust if necessary
      if('STATEFP20' in mdgdf.columns):
         self.rename_columns(mdgdf)      
      
      # Refine Census data for Baltimore Only
      self.gdf = mdgdf.loc[mdgdf['COUNTYFP'] == '510'].to_crs('EPSG:3857')
      
     
      # Rather than calculate in square meters, let's adjust now 
      # so that this is in km^2
      self.gdf['area'] = self.gdf.to_crs('EPSG:6933')['geometry'].area /1E6

      
      #The total area of Baltimore is about 238.41 km^2. Verify
      # base_area = sum(self.gdf[self.gdf['subset']==-1]['area'])
      # subdiv_area = sum(self.gdf[self.gdf['subset']>-1]['area'])  
      # print(f"Calculated {base_area=}")
      # print(f"Calculated {subdiv_area=}")
      # landarea = sum(self.gdf[self.gdf['subset']==-1]['ALAND'])
      # waterarea = sum(self.gdf[self.gdf['subset']==-1]['AWATER'])
      # area = (landarea + waterarea) / 1E6
      # print(f"Census {area=}")

   
   def rename_columns(self,mdgdf):   
      mdgdf.rename(columns = {'STATEFP20':'STATEFP'}, inplace=True)
      mdgdf.rename(columns = {'COUNTYFP20':'COUNTYFP'}, inplace=True)
      mdgdf.rename(columns = {'TRACTCE20':'TRACTCE'}, inplace=True)
      mdgdf.rename(columns = {'BLOCKCE20':'BLOCKCE'}, inplace=True)
      mdgdf.rename(columns = {'GEOID20':'GEOID'}, inplace=True)
      mdgdf.rename(columns = {'NAME20':'NAME'}, inplace=True)
      mdgdf.rename(columns = {'MTFCC20':'MTFCC'}, inplace=True)
      mdgdf.rename(columns = {'UR20':'UR'}, inplace=True)
      mdgdf.rename(columns = {'UACE20':'UACE'}, inplace=True)
      mdgdf.rename(columns = {'UATYPE20':'UATYPE'}, inplace=True)
      mdgdf.rename(columns = {'FUNCSTAT20':'FUNCSTAT'}, inplace=True)
      mdgdf.rename(columns = {'ALAND20':'ALAND'}, inplace=True)
      mdgdf.rename(columns = {'AWATER20':'AWATER'}, inplace=True)
      mdgdf.rename(columns = {'INTPTLAT20':'INTPTLAT'}, inplace=True)
      mdgdf.rename(columns = {'INTPTLON20':'INTPTLON'}, inplace=True)
      mdgdf.rename(columns = {'HOUSING20':'HOUSING'}, inplace=True)
      mdgdf.rename(columns = {'POP20':'POP'}, inplace=True)         
   
   def mapplot(self,axis):
      
      self.gdf.plot(ax=axis,edgecolor="red", facecolor="none", linewidth=1)
      

   def mapplot_geoid(self,axis,geoid):      
      df = self.gdf[self.gdf['GEOID'] == geoid]
      ax = df.plot(ax=axis,edgecolor="red", facecolor="none", linewidth=1, 
                         figsize=(10,10))
   
class mobility_data:
   def __init__(self,mobility_dir,pkl):
      print("Loading Mobility Data")
      
      if Path.exists(pkl):
         self.gdf = pd.read_pickle(pkl)
         print("Mobility Data Loaded")    
      else:
         files = mobility_dir.glob('*.csv')
         df = pd.concat([pd.read_csv(f,dtype={'poi_cbg':'UInt64'}) \
                         for f in files])
         
         # Don't know the CRS for the data. Guess 4326?
         geometry = gpd.points_from_xy(df.longitude, df.latitude)
         temp_gdf = gpd.GeoDataFrame(df,
                                     geometry=geometry,
                                     crs = "EPSG:4326")
         
         # Filter out some of the odd POIs
         # Use data from https://msgic.org/table-of-bounding-coordinates/
         self.gdf = temp_gdf.loc[
            (temp_gdf['latitude'] >= 39.16) &
            (temp_gdf['latitude'] <= 39.40) &
            (temp_gdf['longitude'] >= -76.74) &
            (temp_gdf['longitude'] <= -76.48)]
         
         # Store result as EPSG:3857 (which is how crimes are stored)
         
         self.gdf = self.gdf.to_crs('EPSG:3857')
         print("Pickling Mobility Data")
         pd.to_pickle(self.gdf,pkl)
         print("Mobility Data Loaded")         
         
   def mapplot(self,axis):
      self.gdf.plot(ax=axis,marker='o', markersize=1, color='blue')      
   
class aggregated:
   def __init__(self,mobility,census_block_group):
      print("Aggregating Mobility and Geography")
      
#      print(census_block_group.gdf['GEOID'].unique())
#      print(mobility.gdf['poi_cbg'].unique())
#      print(len(mobility.gdf['poi_cbg'].unique()))

      join = gpd.sjoin(mobility.gdf,census_block_group.gdf)

#      print(join.head())
#      print(join.dtypes)
#      print(len(join))
#      print(len(mobility.gdf))

      filtered_join = join.loc[(join['poi_cbg'] != join['GEOID'])]

#      print(filtered_join.head())
      print(len(filtered_join))

      xls =  (CWD / "filtered.xlsx")   
      filtered_join.to_excel(xls)
      
      
      
      # pivot = pd.pivot_table(join,
      #                        index=['GEOID','subset'],
      #                        columns='Description', 
      #                        aggfunc={'Description':'count'}) 
      # pivot.columns = pivot.columns.droplevel()
      # self.gdf = geoggdf.merge(pivot, how='left', on=['GEOID','subset']) 

      
      
def main():
   bg2010 = census2010(BLOCKGROUP_2010_SHAPEFILE)

   fig, ax1 = plt.subplots(figsize=(30,30))
   fig2, ax2 = plt.subplots(figsize=(30,30))
   bg2010.mapplot_geoid(ax1,245100808002)
   bg2010.mapplot_geoid(ax2,245100807001)
   ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)
   ctx.add_basemap(ax2, source=ctx.providers.OpenStreetMap.Mapnik)
   
#   mobility = mobility_data(MOBILITY_DIR_PATH,MOBILITY_PKL)
#   agg = aggregated(mobility,bg2010)   


#   fig, ax1 = plt.subplots(figsize=(30,30))
#   bg2010.mapplot(ax1)
#   ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)
   
#   mobility = mobility_data(MOBILITY_DIR_PATH,MOBILITY_PKL)
#   bg = census(BLOCKGROUP_SHAPEFILE) 
#   agg = aggregated(mobility,bg)
   
#   fig, ax1 = plt.subplots(figsize=(30,30))
#   bg.mapplot_geoid(ax1,'245101903001')
#   ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)

#   fig, ax1 = plt.subplots(figsize=(15,15))
#   mobility.mapplot(ax1)
#   ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)

#   crime = crimes(CRIME_XLS,CRIME_XLS_SHEET_NAME,CRIME_PKL)
  
   
#   fig, ax1 = plt.subplots(figsize=(15,15))

#   bg.mapplot(ax1)   
#   crime.mapplot(ax1,crimetype='BURGLARY')
#   ctx.add_basemap(ax1, source=ctx.providers.OpenStreetMap.Mapnik)

if __name__ == "__main__":
   main()
         