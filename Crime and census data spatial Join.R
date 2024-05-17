##*****Joining Crime and Census data*******
  ##*This program takes the filtered crime and census data and 
  ##* merges them via spatial join.

##****Note: To run for a different census region upload the corresponding files***
###****into md_shape variable and change shape variable to reflect region type***

#Import libraries
library(sf)
library(dplyr)
library(readxl)
library(ggplot2)

#Initate variables
  #md census region
  md_region = "tl_2022_24_tract.shp"

  #cleaned crime data
  crime = "Cleaned_Crime_Data2.Feb7.csv"
  
  #Desired shape file name
  shape = "baltimore_crime.shp"

  #county code
  cc = 510
  
#Import data sets
  #import cleaned crime data
  crime.df = read.csv(crime)
    
  #import census data
  md_region = st_read(md_region)
  
#Filter census data to only include the desired county (cc)

balt_region = md_region %>%
  filter(COUNTYFP == cc)

#Graph the obtained region
ggplot() + geom_sf(data = balt_region)

##Spatial join data sets 

#Create a geo data frame(gdf) of the cleaned crime data
  #takes the crime df and its (long,lat) and maps it onto the 
  #the baltimore tracts coordinate reference system(crs)
crime.gdf = st_as_sf(crime.df, coords = c("Longitude","Latitude"),
                     crs = st_crs(balt_region))

#Creates the crime.gdf into a shape file and saves it
crime_region = st_write(crime.gdf, shape, append=FALSE)


#Merge crime data and census tract data 
crimeRegion_join = st_join(balt_region,crime_region, join = st_intersects)

#View new columns names to confirm merge
colnames(crimeRegion_join)

#Used as checkpoint
# #Create an excel file of the merged data 
# #excel
# write_xlsx(crimeTract_join, "Crime_Tract_Spatial_Join_extra_LatLon.xlsx")
# 
# #csv
# write.csv(crimeTract_join, "Crime_Tract_Spatial_Join_extra_LatLon.csv", row.names = FALSE)
# 
# #Create a shape file of the joing
# 
# st_write(crimeTract_join, "baltimore_crime_tract_join_extra_LatLon.shp", append=FALSE)



