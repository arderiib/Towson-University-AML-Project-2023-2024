####***Cleaning the Crime Data*
##** The following program imports baltimore city crime data and cleans it for 
##* use in future programs. 

#Import libraries
library(dplyr)
library(writexl)

#initiate variables
  #crime data file name
  crime = "crime_data.csv"
  
  #cut off date for data set
  cutOff = "2015/01/01"


#import crime data
crime.df1 = read.csv(crime)

#filter out invalid Latitudes, Longitudes, and geolocations
  #Latitudes,Longitudes, geolocations; removes 0's and NA's
  crime.df2 = crime.df1[(crime.df1$Latitude[]) != 0 & (crime.df1$Longitude[]) != 0 
                        & complete.cases(crime.df1$Longitude[]) != FALSE & complete.cases(crime.df1$Latitude[]) != FALSE,]
  
  
  
  #Filter out longitude <-76.5 and longitude > -76.72 (based on map of Baltimore city)
  # and remove unecessary columns
  crime.df3 = crime.df2 %>% filter(Longitude > -76.72 & Longitude < -76.5) %>% 
    select(-c(Inside_Outside), -c(Weapon), -c(Gender), -c(Age), 
           -c(Race), -c(Ethnicity), -c(Total_Incidents), -c(Post), -c(Premise), -c(District)) %>%
    mutate_all(toupper)

#Ensure NA entries from the filtered data have been removed
crime.df3 = crime.df3[complete.cases(crime.df3[]) != FALSE,]

#Used as checkpoint
# #Remove unnecessary columns for out purposes
# #Retrieve column names 
# colnames(crime.df3)

#Filter out irrelevent data
  #Invalid dates/ times
    #find the min and max of the Crime date/time
    date_min = min(crime.df3$CrimeDateTime)
    date_max = max(crime.df3$CrimeDateTime)

    #create a date variable to view all dates
    date = unique(crime.df3$CrimeDateTime)

      #Sort the array date in ascending order
      date_sorted_increasing = sort(date, decreasing = FALSE)
      print(date_sorted_increasing)
      
      #sort the array date in descending order
      date_sorted_decreasing = sort(date, decreasing = TRUE)
      print(date_sorted_decreasing)

  #remove dates that are invalid; 
  #i.e the year 1023, 1202, and 1922 and dates prior to 2015 to reduce file size
  crime.df4 = crime.df3 %>% filter(crime.df3$CrimeDateTime >= cutOff) 

  #confirm correct dates were removed 
  newDates = unique(crime.df4$CrimeDateTime)
  sortNewDates = sort(newDates)
  print(sortNewDates)  


#Used as checkpoint
# #create a new csv and excel file for the sorted data 
# #csv file
# write.csv(crime.df4, file="Cleaned_Crime_Data2.csv", row.names = FALSE)
# 
# #excel file
# write_xlsx(crime.df4, "Cleaned_Crime_Data2.xlsx")
# 
