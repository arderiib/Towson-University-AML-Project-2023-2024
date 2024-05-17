###***Sectioning crime and mobility by month***###
##*** This program takes in mobility and crime data and separates the respective
##*data frames by month. These are then saved as excels which will be utilized in 
##*later programs.
##*
##*

#Libraries
library(readxl)
library(dplyr)


#Initialize variables
  #Crime data file name
  crime = "Cleaned_Crime_Data2.Feb7.csv"
  
  #Create a string of all the dates
  months = c("2018/01/01", "2018/02/01", "2018/03/01", "2018/04/01", "2018/05/01", "2018/06/01",
             "2018/07/01", "2018/08/01", "2018/09/01", "2018/10/01", "2018/11/01", "2018/12/01",
             "2019/01/01", "2019/02/01", "2019/03/01", "2019/04/01", "2019/05/01", "2019/06/01",
             "2019/07/01", "2019/08/01", "2019/09/01", "2019/10/01", "2019/11/01", "2019/12/01",
             "2020/01/01", "2020/02/01", "2020/03/01", "2020/04/01", "2020/05/01", "2020/06/01",
             "2020/07/01", "2020/08/01", "2020/09/01", "2020/10/01", "2020/11/01", "2020/12/01",
             "2021/01/01", "2021/02/01", "2021/03/01", "2021/04/01", "2021/05/01", "2021/06/01",
             "2021/07/01", "2021/08/01", "2021/09/01", "2021/10/01", "2021/11/01", "2021/12/01",
             "2022/01/01", "2022/02/01", "2022/03/01", "2022/04/01", "2022/05/01", "2022/06/01",
             "2022/07/01", "2022/08/01", "2022/09/01", "2022/10/01", "2022/11/01", "2022/12/01","2023/01/01")
  
#import the crime data
crime.df1 = read.csv(crime)

#Initialize data frame 
monthNumCrime.df = matrix()
monthNumCrime.df = data.frame()


#####Creates a function to create a table for the number of crimes in a month for each crime#############

monthFunct = function(monthStart, monthEnd){
  
  #create a list containing the crime descriptions 
  crimeType = table(crime.df1$Description)
  crime.list = names(crimeType)
  
  #Create a data frame for the output
  #it's important to list the type since otherwise i encounter errors 
  output = data.frame(month = character(),
                      crime.type = character(),
                      total.crimes = numeric(),
                      stringsAsFactors = FALSE)
  
  
  #filter crime for the selected date range
  crime.df2 = filter(crime.df1, crime.df1$CrimeDateTime >= monthStart & crime.df1$CrimeDateTime <= monthEnd)
  
  #Create a for loop to run each crime in crime.list sequentially
  for (i in seq_along(crime.list)) {
    
    # Filter for a particular crime in the selected date range
    crime.df3 = filter(crime.df2, Description == crime.list[i])
    
    # Find the number of crimes that occurred that date range
    crime.count = nrow(crime.df3)
    
    # Pull the month info
    currentMonth = substr(monthStart, start = 1, stop = 7)
    
      
      # Store data into a data frame 
      results = data.frame(month = currentMonth,
                           crime.type = crime.list[i],
                           total.crimes = crime.count,
                           stringsAsFactors = FALSE)
    #confirm output
    print(results)
    
    #Put results into a dataframe 
    output = rbind(output, results)
  }
  return(output)
}

#Create a for loop to go through each month and save the results 
for (i in 1:(length(months)-1)) {
  monthStart = months[1]
  monthEnd = months[1+1]
  monthData = monthFunct(monthStart, monthEnd)
  monthNumCrime.df = rbind.data.frame(monthNumCrime.df, monthData)
}


#Used as checkpoint
# #Export into an excel and csv for later use 
# ###****Change the title of excel and csv file to desired name**
# #excel
# write_xlsx(monthNumCrime.df, "2018_2022_total_individual_crime_by_month.xlsx")
# 
# #csv
# write.csv(monthNumCrime.df, "2018_2022_total_individual_crime_by_month.csv")

