####**Computing quadrat analysis and the Chi^2 for each census region***
##* This program conducts a quadrat analysis using the crime data. The program then
##* calculates the chi^2, p-value, the # of points that are significant/not
##* significant/NA , The # of points percentages (pecentage of significant/not significant
##*  / NA), and exports all of the intermediary steps as csv/excel's to reduce the 
##*  running time when recaluclating. Majority of the operations are functions, 
##*  so when finding for different regions there is limited amounts of entries that 
##*  need to be changed. 
##*  


#import library
library(spatstat)
library(ggplot2)
library(sf)
library(dplyr)
library(readxl)
library(writexl)

#initialize variables
  #Baltimore shape file 
  balt_region = "baltimore_tract.shp"
  
  #Crime and census data join
  crime_census_join = "baltimore_crime_tract_join.shp"
  
  
  #start and end date for data set filtration
  startRange =  "2015/01/01"
  endRange ="2023/01/01"
  
  #Quadrat Grid size ( m by n grid)
  m = 4
  n = 4

  #Import data 
    #baltimore shape data
    balt_region = st_read(balt_region)
    
    #crime census data
    original_balt_crime = st_read(crime_census_join)

#Initialize data frames for storing results 
    #filter crime data for desired date range 
    balt_crime = original_balt_crime %>% filter(CrmDtTm >= startRange & CrmDtTm <= endRange )
    
    #create a list containing the crime descriptions 
    crimeType = table(balt_crime$Dscrptn)
    crime.list = names(crimeType)
    
    #create a list containing the different tracts 
    regionType = table(balt_crime$TRACTCE)
    region.list = names(regionType)
    
    #output data frame
    output = matrix(NA, nrow= length(crime.list)* length(region.list), ncol = 7)
    output = data.frame()
    
    
    
    
    
#Function to pull coordinates

get.coords<-function(location_str){ 
  
  # Remove parentheses and split the string into latitude and longitude parts
  parts <- unlist(strsplit(gsub("[()]", "", location_str), ","))
  
  # Convert the parts to numeric
  numeric_location <- as.numeric(parts)
  
  # Check the result
  return(numeric_location)
}



###########################
# pick a crime, tract, and a year

##**SECTION NOTE** : These for loops cycle through each census region and each crime 
##* then filters the shape files and crime data. This is used to create a ppp to conduct
##*  the quadrat analysis via the quadrat.test.quadratcount() function. 
##*  The loop filters the shape file to the desired census region and the non-shape
##*  file that contains the crime data so it only contains points within the desired census region.
##*  The program then plots the points into the window, which is the shape file, 
##*  and creates a ppp object in which the quadrat analysis is conducted on.
##*  Results are then saved into excels and csv to cut down on processing time for future use. 

for ( i.region in 1:length(region.list)){ 
  for ( i.crime in 1:length(crime.list)){
    
    #filter the balt_ tract to the region.list
    new_balt_region = filter(balt_region, balt_region$TRACTCE == region.list[i.region])
    
    #filter the balt_region to the parameters you want
    new_balt_crime <- balt_crime %>% filter(Dscrptn == crime.list[i.crime])
    
    # #plot new_balt_region
    # ggplot() + geom_sf(data = new_balt_region)
    # 
    # #get crime location
    # ggplot() + geom_sf(data = new_balt_crime)
    
    
    #Function call
    get.coords(new_balt_crime$GeoLctn)
    
    #Get the crime coordinates
    crime.coords.2 <- lapply(new_balt_crime$GeoLctn, FUN=get.coords)
    crime.coords.2 <- matrix(unlist(crime.coords.2), ncol=2, byrow=TRUE)
    
    
    #Get census tract coordinates for window
    tract_coords.2 = st_coordinates(new_balt_region)
    
    
    # Create a polygonal window
    tract_window.2 <- owin(poly =  tract_coords.2[,c(2,1)])
    
    #print(tract_window.2)
    #plot(tract_window.2)
    
    #Create a ppp
    data.ppp.2 <- as.ppp(crime.coords.2,  W = tract_window.2)
    
    #print(data.ppp.2)
    #plot(data.ppp.2)
    
    #Do the quadrat count
    q.2 = quadratcount.ppp(data.ppp.2, nx = m, ny = n)
    
    #summary(q.2)
    print(q.2)
    #plot(q.2)
    
    #Find the Chi square for each tract
    chi.2 = quadrat.test.quadratcount(q.2, alternative = "two.sided")
    
    #plot(chi.2)
    #summary(chi.2)
    print(chi.2)
    
    #Create a table to display information
    results = c("Crime Type" = crime.list[i.crime], "Tract ID" = region.list[i.region],"Chi^2" = round(chi.2$statistic, digits = 4),
               "Two-sided P-value"= round(chi.2$p.value, digits = 4),"Right-tail P.Value" = round(chi.2$p.value/2, digits = 4))
    print(results)
    output = rbind.data.frame(output, results)
    
    
  }#end of crime
}#end of tract

#Rename to proper column names 
colnames(output) = c("Crime.Type", "Tract.ID", "Chi.2", "Two.Sided.P.value", "Right.P.value")


# #Used as checkpoint
# #Verify output
# colnames(output)
# 
# #Export to excel
# write_xlsx(output, "2015_2023_Chi^2_Report.xlsx")
# 
# #Export as a csv
# write.csv(output, "2015_2023_Chi^2_Report.csv")

############################################################################################

#*****finding the significance for each crime in a give year*
  ##The following results in a matrix that contains the significance for 
  ## a each crime across all census tracts in a given year. 

#Initiate variables
  #Chi^2 report files
    #reports for individual years
    chi_report_2015 = "2015_Chi^2_Report.csv"
    chi_report_2016 = "2016_Chi^2_Report.csv"
    chi_report_2017 = "2017_Chi^2_Report.csv"
    chi_report_2018 = "2018_Chi^2_Report.csv"
    chi_report_2019 = "2019_Chi^2_Report.csv"
    chi_report_2020 = "2020_Chi^2_Report.csv"
    chi_report_2021 = "2021_Chi^2_Report.csv"
    chi_report_2022 = "2022_Chi^2_Report.csv"
    
    #reports for aggregated results
    chi_aggregated_report = "2015_2023_Chi^2_Report.csv"
    
  #Number of census regions
  region = 199
    

#Import chi^2 reports
  #chi^2 reports for individual years
  chi_2015 = read.csv(chi_report_2015)
  chi_2016 = read.csv(chi_report_2016)
  chi_2017 = read.csv(chi_report_2017)
  chi_2018 = read.csv(chi_report_2018)
  chi_2019 = read.csv(chi_report_2019)
  chi_2020 = read.csv(chi_report_2020)
  chi_2021 = read.csv(chi_report_2021)
  chi_2022 = read.csv(chi_report_2022)
  
  #aggregated chi^2 report
  chi_2015_2023 = read.csv(chi_aggregated_report)
  
  #Chi years labels
  chiYR1 = "2015_chi"
  chiYR2 = "2016_chi"
  chiYR3 = "2017_chi"
  chiYR4 = "2018_chi"
  chiYR5 = "2019_chi"
  chiYR6 = "2020_chi"
  chiYR7 = "2021_chi"
  chiYR8 = "2022_chi"
  
  chiYRall = "2015_2023_chi"

#Initialize data frames
#chi^2 stats results data frame 
chi_matrix0 = matrix(NA, nrow= length(crime.list), ncol = 12)
chi_matrix0 = data.frame()



#Create a function to call to get the significance matrix
chi_funct = function(chi_year,crime_num,chi_year_title){
  
  i.crime = crime_num
  
  #filter based on crime type for all tracts in the selected year
  avg_Chi.df1 = filter(chi_year, chi_year$Crime.Type == crime.list[i.crime])
  
  
  #**IMPORTANT**: The NA P-Values are filtered out since there is not enough info
  #*to say that whether they're significant or not. However the NA P-values
  #*to state the proportion of data points that couldn't calculate a p-value
  #*(This also means that there were no points in that quadrat so there is no
  #*chi^2 value for that quadrat). Since they're still important and it's easier 
  #*to keep something and not need it than get rid of it an need it later. 
  
  #Create a columns for:
    #Number of Significant P-Values
    avg_Chi.df1$Significant.P.values
  avg_Chi.df1[1, "Significant.P.values"] = sum(avg_Chi.df1$Right.P.value <0.05, na.rm=TRUE)
  
  
    #Percentage of significant P-values rounded to 4 digits of accuracy
    avg_Chi.df1$Significant.Percentage
    
    avg_Chi.df1[1, "Significant.Percentage"] = round(
      (avg_Chi.df1[1, "Significant.P.values"]/region)*100, digits = 4)
    
    #Number of Not Significant P-Values 
    avg_Chi.df1$Not.Significant.P.values
    avg_Chi.df1[1, "Not.Significant.P.values"] = sum(avg_Chi.df1$Right.P.value>=0.05, na.rm=TRUE)
    
    #Percentage of not significant P-values rounded to 4 digits of accuracy
    avg_Chi.df1$Not.Significant.Percentage
    
    avg_Chi.df1[1, "Not.Significant.Percentage"] = round(
      (avg_Chi.df1[1, "Not.Significant.P.values"]/region)*100, digits = 4)
    
    #Number of NA P-values
    avg_Chi.df1$NA.P.values
    avg_Chi.df1[1, "NA.P.values"] = sum(is.na(avg_Chi.df1$Right.P.value))
    
    #Percentage of NA P-values rounded to 4 digits of accuracy
    avg_Chi.df1$NA.Percentage
    
    avg_Chi.df1[1, "NA.Percentage"] = round(
      (avg_Chi.df1[1, "NA.P.values"]/region)*100, digits = 4)
    
  #Create the filenames
  prefix = chi_year_title
  suffix = avg_Chi.df1[1, "Crime.Type"]
  
    #excel
    excel_Name = paste0(prefix, "_", suffix, ".xlsx" )
    
    #csv
    csv_Name = paste0(prefix, "_", suffix, ".csv")
    
  #Create a table to display information
  chi_matrix0 = rbind.data.frame(chi_matrix0, avg_Chi.df1)
  
  #Export into an excel 
  write_xlsx(chi_matrix0, excel_Name)
  
  #Export into a csv
  write.csv(chi_matrix0, csv_Name)
  
  return(chi_matrix0)
}

#Create a function to loop through the chi_funct for all crimes in a given year
cycle_funct = function(chi_years, chi_years_label){
  for (i in 1:13)
  {
    chi_funct(chi_years,i, chi_years_label)
  }
  return()
}

#run the cycle function for each year
cycle_funct(chi_2015, chiYR1)
cycle_funct(chi_2016, chiYR2)
cycle_funct(chi_2017, chiYR3)
cycle_funct(chi_2018, chiYR4)
cycle_funct(chi_2019, chiYR5)
cycle_funct(chi_2020, chiYR6)
cycle_funct(chi_2021, chiYR7)
cycle_funct(chi_2022, chiYR8)

#run the cycle function for 2015-2023
cycle_funt(chi_2015_2023, chiYRall)


################################################################
#Create a function to pull a particular years overall significance data 


#Declare the matrix 
chi_matrix1 = matrix(NA, nrow= length(crime.list), ncol = 10)
chi_matrix1 = data.frame()

search_funct = function(chi_prefix){
  
  #The for loop cycles through each of the 13 crime types 
  for (i in 1:13){
    i.crime = crime.list[i]
    csv_Name = paste0(chi_prefix, "_", i.crime, ".csv")
    
    #Create a new csv name
    new_csv_Name = paste0(chi_prefix,"_Significance" ,".csv" )
    
    #Create a new excel name
    new_excel_Name = paste0(chi_prefix, "_Significance" ,".xlsx" )
    
    
    current_chi = read.csv(csv_Name)
    
    
    #Create a table to display information
    overall_chi = c(current_chi[1,"Crime.Type"], current_chi[1, "Significant.Percentage"],
                    current_chi[1, "Not.Significant.Percentage"],
                    current_chi[1, "NA.Percentage"],
                    current_chi[1, "Significant.P.values"],
                    current_chi[1, "Not.Significant.P.values"],
                    current_chi[1, "NA.P.values"])
    
    #print(overall_chi)
    
    #Save overall_chi into a new matrix
    chi_matrix1 = rbind.data.frame(chi_matrix1, overall_chi)
  }
  
  
  #relabel colnames for chi_matrix1
  colnames(chi_matrix1) = c("Crime Type", "Significant Percentage",
                            "Not Significant Percentage", "NA Percentage", 
                            "# of Significant P-values", "# of Not Significant P-Values",
                            "# of NA P-Values")
  
  
  #Create a csv and excel for the final table 
  #Export into an excel 
  write_xlsx(chi_matrix1, new_excel_Name)
  
  #Export into a csv
  write.csv(chi_matrix1, new_csv_Name)
  
  return(chi_matrix1)
}

#run through the search_funct for each year   
search_funct(chiYR1)
search_funct(chiYR2)
search_funct(chiYR3)
search_funct(chiYR4)
search_funct(chiYR5)
search_funct(chiYR6)
search_funct(chiYR7)
search_funct(chiYR8)

#run throught the search_funct for 2015-2023
search_funct(chiYRall)

