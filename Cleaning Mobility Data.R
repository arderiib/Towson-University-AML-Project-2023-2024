###***Cleaning the Mobility Data##***##
#* The following program will read the mobility data and filter it 
#* to contain only relevant information. In addition, each year of data will be 
#* merged into one large data set for later use.

#import libraries
library(dplyr)
library(readxl)
library(writexl)

#Initialize mobility join dataframe
output.df = data.frame()


#Initiate variables
  #mobility month file name
  mobility1 = "Baltimore_2021_01.csv"
  mobility2 = "Baltimore_2021_02.csv"
  mobility3 = "Baltimore_2021_03.csv"
  mobility4 = "Baltimore_2021_04.csv"
  mobility5 = "Baltimore_2021_05.csv"
  mobility6 = "Baltimore_2021_06.csv"
  mobility7 = "Baltimore_2021_07.csv"
  mobility8 = "Baltimore_2021_08.csv"
  mobility9 = "Baltimore_2021_09.csv"
  mobility10 = "Baltimore_2021_10.csv"
  mobility11 = "Baltimore_2021_11.csv"
  mobility12 = "Baltimore_2021_12.csv"

  #Final mobility data name 
  baltMob.csv = "2018_2022_Cleaned_Baltimore_Mobility.csv"
  baltMob.xlsx = "2018_2022_Cleaned_Baltimore_Mobility.xlsx"
  

mobilityJoinFunct = function(){
  
  #Initialize mobility dataframe 
  mob.df = data.frame()

  #import mobility file for a given year
  mob1  = read.csv(mobility1)
  mob2  = read.csv(mobility2)
  mob3  = read.csv(mobility3)
  mob4  = read.csv(mobility4)
  mob5  = read.csv(mobility5)
  mob6  = read.csv(mobility6)
  mob7  = read.csv(mobility7)
  mob8  = read.csv(mobility8)
  mob9  = read.csv(mobility9)
  mob10  = read.csv(mobility10)
  mob11  = read.csv(mobility11)
  mob12  = read.csv(mobility12)


#Merge new data sets and store into mob.df
mob.df = rbind.data.frame(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8,
                           mob9, mob10, mob11, mob12)

mob.df1 =  mob.df %>% select(latitude,longitude,date_range_start,date_range_end,
                             raw_visit_counts,raw_visitor_counts)

output.df = rbind(output.df,mob.df1)


return(output.df)
}

#run the mobility function for each new year
###***Note: must change reinitiate the mobility variables to reflect the new year each time*
###**You run the mobility function **
join2018 = mobilityJoinFunct()
join2019 = mobilityJoinFunct()
join2020 = mobilityJoinFunct()
join2021 = mobilityJoinFunct()
join2022 = mobilityJoinFunct()

mobility.df1 = rbind.data.frame(join2022,join2021,join2020,join2019,join2018)

# #Used as Checkpoint
# # Save the filtered.df1 as an excel and a csv
# write.csv(filteredMob, "2018_2022_Cleaned_Baltimore_Mobility.csv")
# write_xlsx(filtered.df1, "2018_2022_Cleaned_Baltimore_Mobility.xlsx")
# 

