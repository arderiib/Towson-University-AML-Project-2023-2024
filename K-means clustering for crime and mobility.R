###***K-means clustering for crime and mobility***###
##*** This program takes in mobility and crime data,which has already been filtered
##* by month,and joins these two dataset's to create a new data frame to conduct 
##* the k-means clustering analysis on. The k-means clustering analysis is done for
##* all crimes and each unique type of crime. The results are then plotted on a graph
##* and automatically exported to the selected folder, for later use.



#import libraries
library(readxl)
library(writexl)
library(dplyr)
library(ggplot2)


#initiate variables
  #Files in csv format
    #mobility file
    mobility = "2018_2022_total_raw_visits_by_month.csv"

    #crime file
    crime = "2018_2022_total_individual_crime_by_month.csv"

  #Cut off dates Covid-19 pandemic
    #pre-covid 
    pre_covid = "2020/03"
    
    #post-covid
    post_covid = "2020/04"

#import data sets
#****change the file names for mobility.df1, crime.df1, to the file you named earlier**
  #mobility data by month
  mobility.df1 = read.csv(mobility)

  #crime data by month
  crime.df1 = read.csv(crime)


#create a list containing the crime descriptions 
crimeType = table(crime.df1$crime.type)
crime.list = names(crimeType)


###################################################################################################

#Join the crime and mobility data
  #Create a data frame to store the final output
  mobMonthCrimeType.df1 = matrix()
  mobMonthCrimeType.df1 = data.frame()

#filter for each crime type and merge the data sets
for (i in seq_along(crime.list)) {
  
  crime.df2 = filter(crime.df1, crime.type == crime.list[i])
  
  #Add a column X that numbers the rows sequentially
  crime.df2 = crime.df2 %>% mutate(X = row_number())
  
  #Join the crime and mobility data by the column X  
  mobMonth.df = full_join(crime.df2,mobility.df1, by = ("X" = "X"))
  
  mobMonthCrimeType.df1 = rbind(mobMonthCrimeType.df1,mobMonth.df)
}


#Used as Checkpoint
# #Save data frame as a csv and excel for later use 
#   #excel
#   write_xlsx(mobMonthCrimeType.df1, "2018_2022_mob_crime_by_month.xlsx")
#   #csv
#   write.csv(mobMonthCrimeType.df1, "2018_2022_mob_crime_by_month.csv")

#############################################################################################3333

#Do the k means clustering for each crime type 

#Filter columns to just include crime and mobility 
 #For saving the kmeans info into data frames add 'x' ,'crime.type' ,and 'months' to select
#do this after you run the kmeans function

#allCrimes
#***Needs to be fixed, doesn't work ****
  mobMonthCrime.df0 = mobMonthCrime.df1 %>% select(X,crime.type, month.x, total.crimes, total.raw.visits)
  #filter to run each cluster analysis
  kmeans0 = mobMonthCrimeType.df1 %>%
    select(X, total.crimes, total.raw.visits)
  kmeans.df0 = kmeans(kmeans0,2)
  kmeans.df0 = kmeans(mobMonthCrime.df0,2)

#Create data frames for kmeans results
  #kmeans.df
  kmeansResults.df = matrix()
  kmeansResults.df = data.frame()
  
  
for(i in seq_along(crime.list)){
  
  #filter for current crime type
  mobMonthCrime.df = mobMonthCrimeType.df1 %>%
    filter(crime.type == crime.list[i]) %>% select(X,crime.type, month.x, total.crimes, total.raw.visits)
  
  #Prepare data for cluster analysis
  kmeansPrep.df = mobMonthCrimeType.df1 %>%
    filter(crime.type == crime.list[i]) %>% select(X, total.crimes, total.raw.visits)
  
  #Perform cluster analysis
  kmeans.df = kmeans(kmeansPrep.df,2)
  
  #Store results into final table
  kmeansResults.df = rbind(kmeansResults.df, cbind(cluster = kmeans.df$cluster,
                                       center.x = round(kmeans.df$centers[kmeans.df$cluster, 1], digits = 4),
                                       center.y = round(kmeans.df$centers[kmeans.df$cluster, 2], digits = 4),
                                       X = mobMonthCrime.df$X,
                                       crime.type = mobMonthCrime.df$crime.type,
                                       month = mobMonthCrime.df$month.x,
                                       total.raw.visits = mobMonthCrime.df$total.raw.visits,
                                       total.crimes = mobMonthCrime.df$total.crimes
                                       ))
  
  
}

# #Checkpoint to save data
# #save as an excel and a csv
#   #excel
#   write_xlsx(totalKmeans.df1, "2018_2022_kmeans_individual_crime_by_month.xlsx")
# 
#   #csv
#   write.csv(totalKmeans.df1, "2018_2022_kmeans_individual_crime_by_month.csv")

  
############################################################################################################   
#####***Check point: Bug free until this point*****
##Compute the Chi^2 for clustered crimes and for each crime type ##     

##Create a dataset that filters the kmeans data by date and cluster number

#Filter for pre and post covid
  #Filter for pre-covid 
  clusteredPre.df1 = kmeansResults.df %>% filter(month <= pre_covid ) %>%
    group_by(month,cluster,crime.type)


  #Filter for post-covid 
  clusteredPost.df1 = kmeansResults.df %>% filter(month >= post_covid) %>% 
    group_by(month,cluster,crime.type)


#Create a function that takes a data frame then counts all the points that 
#happened in  a cluster for a particular crime and places it into a new table 

cluster.funct = function(clusteredData, dateRange){
  #get the data frame and filter it based on crime type
  
  #Initialize data frame for cluster Analysis results
  clusterAnalysis.df1 = matrix()
  clusterAnalysis.df1 = data.frame()
  
  #filter for each crime type and merge the data sets
  for (i in seq_along(crime.list)) {
    
    filteredCrime.df1 = clusteredData %>% filter(crime.type == crime.list[i]) %>% 
      group_by(cluster)
    
    #Create a new date column with the captured time frame
    date = dateRange
    
    #Get the sum for the number of points in that cluster 
    
    cluster.countA =  sum(filteredCrime.df1$cluster == 1)
    cluster.countB =  sum(filteredCrime.df1$cluster == 2)
    
    #Create a table containing the date range(i.e pre/post covid), crime type, 
    #and cluster count for that cluster
      
      #Create a data frame containing the desired columns 
      contingencyTable.1 = data.frame( crime.list[i],date, cluster.countA, cluster.countB)
      
      #Merge into an output table
      clusterAnalysis.df1 = rbind(clusterAnalysis.df1,contingencyTable.1)
  }
  
  return(clusterAnalysis.df1)
}


#Filter for pre and post covid
  #Filter for pre-covid 
  clusteredPre.df1 = kmeansResults.df %>% filter(month <= pre_covid ) %>%
    group_by(month,cluster,crime.type)
  
  
  #Filter for post-covid 
  clusteredPost.df1 = kmeansResults.df %>% filter(month >= post_covid) %>% 
    group_by(month,cluster,crime.type)

#Run the cluster.funct for each date range NOTE: 3/2020 is included in pre and 4/2020 is included in post
clusterTable.Pre = cluster.funct(clusteredPre.df1, "pre-covid")
clusterTable.Post = cluster.funct(clusteredPost.df1, "post-covid")



#Do a chi square analysis on data
  #Create a data frame to store the final output
  chi2Analysis.df1 = matrix()
  chi2Analysis.df1 = data.frame()


for(i in seq_along(crime.list)){
  #filter the data sets for each crime for pre and post covid
  clusteredCrimePre.df1 = clusterTable.Pre %>% filter(crime.list.i.== crime.list[i])
  clusteredCrimePost.df1 = clusterTable.Post %>% filter(crime.list.i. == crime.list[i])
  
  #join the filtered crime data so pre and post are in a table together
  observedClusters.df1 = full_join(clusteredCrimePre.df1, clusteredCrimePost.df1)
  
  #print to ensure tables are accurate
  print(observedClusters.df1)
  
  #clean tables for chisq.test() function
    #remove the first two columns 
    observedClusters.df2 = observedClusters.df1[,-c(1,2)]
    print(observedClusters.df2)
  
    #format data so its a table
      observedClusters.df3 = as.matrix.data.frame(observedClusters.df2)
      observedClustersTable.df1 = as.table(observedClusters.df3)
  
  #run chi squared test
  clusteredChi2.df1 = chisq.test(observedClustersTable.df1)
  print(clusteredChi2.df1)
  
  #place results into a dataframe to access later
  chi2Table = data.frame(crime.type = crime.list[i], chi2.value = clusteredChi2.df1$statistic, p.value = clusteredChi2.df1$p.value)
  
  chi2Analysis.df1 = rbind(chi2Analysis.df1, chi2Table)
}


#View the cluster analysis data frame
View(chi2Analysis.df1)

  #Create an exportable table
  library(knitr)
  library(kableExtra)
  
  #Change column names to look neat
  cleanedChi2Analysis = chi2Analysis.df1 %>% 
    rename("\u03C7 \u00B2 Value" = chi2.value) %>% 
    rename("p-Value" = p.value) %>% 
    rename ("Crime Type" = crime.type)
  
  
  table = kable(cleanedChi2Analysis, format = "latex", caption = "Cluster \u03C7 \u00B2 Analysis",digits = 20) %>%
    kable_styling(full_width = FALSE)


#Checkpoint for data retention
# #Save cluster analysis data frame into a csv and excel
#   #Excel 
#   write_xlsx(clusteredAnalysis.df2, "clustered_chi2_Analysis_results.xlsx")
#   
#   #csv
#   write.csv(clusteredAnalysis.df2, "clustered_chi2_Analysis_results.csv")


####****Check point: Bug free completely; data shows that they're statistically significant and that there is a relationship**
#################################################################################################################
#plot the kmeans for each crime type  


for(i in seq_along(crime.list)){
#Graphs for k means clustering analysis
  kmeansPlot.df = kmeansResults.df %>% filter(crime.type == crime.list[i])
  mobMonthCrimeType.df2 = mobMonthCrimeType.df1 %>% filter(crime.type == crime.list[i])

  plot = ggplot(mobMonthCrimeType.df2, aes(x = total.raw.visits, y = total.crimes, color = factor(kmeansPlot.df$cluster), shape = ifelse(month.x <= pre_covid, "Pre-COVID", "Post-COVID"))) +
    geom_point() +
    labs(x = "Total Raw Visits",
         y = "Total Crimes",
         title =  paste0("Cluster Analysis for ",crime.list[i]),
         color = "Clusters") +
    scale_x_continuous(labels = scales::scientific_format()) +
    scale_shape_manual(values = c("Pre-COVID" = 16, "Post-COVID" = 17), name = "Date") +  # Define shape for each category
    guides(color = guide_legend(title = "Clusters"), shape = guide_legend(title = "Date"))  # Show only color and shape legends

  ggsave(paste0("cluster_analysis_",crime.list[i],"_plot.png"),width = 5.32 , height = 3.51, plot)
  
}

    



















############################################################################################################# 
#Linear regression for each crime based on cluster 
#make a function that takes the pre or post covid data and takes each cluster
#and does an lm and plots that lm in a graph

something = read.csv("clustered_chi2_Analysis_results.csv")

crimeType = table(crime.df1$Description)
crime.list = names(crimeType)

lmClusteredFunct = function(covidData.df1){
  
  #read data set
  clusteredData = covidData.df1
  
  #Create a data frame to store the final output
  clusteredCorr.df1 = matrix(NA, nrow=780, ncol = 3)
  clusteredCorr.df1 = data.frame()
  
  
  for(i in seq_along(crime.list)){
    
    #initialize raw crime.type 
    crime.type = crime.list[i]
    
    #create a png save file for cluster 1
    pngA = paste0("rawVisitors_vs_", crime.type, "_clusterA.png")
    pngB = paste0("rawVisitors_vs_", crime.type, "_clusterB.png")
    
    #read data set
    clusteredData = clusteredPre.df1
    
    #Create a title name for graph 
    titleNameA = paste0("Total Raw Vistors vs number of ", crime.type," for cluster A")
    
    titleNameB = paste0("Total Raw Vistors vs number of " ,crime.type,"for cluster B")
    
    #run an lm based on each cluster
    #sort by cluster and crime
    clusterA = clusteredData %>% filter(crime.type == crime.list[1]) %>% filter(cluster == "1")
    clusterB = clusteredData %>% filter(crime.type == crime.list[1]) %>% filter(cluster== "2")
    
    
    #cluster linear regressions
    lmA = lm(total.crimes ~ total.raw.visits, data = clusterA)
    lmB = lm(total.crimes ~ total.raw.visits, data = clusterB)
    
    #Plot clusters with lm
    png(pngA)
    #cluster A
    plot(clusterA$total.raw.visits, clusterA$total.crimes,
         xlab = "total Number of Raw Visits",
         ylab = "Total Number of Crimes",
         main = titleNameA)
    
    #Plot linear regression
    abline(lmA, col = "red")
    
    # #print the equation on graph
    # ####***Doesn't look right but I'll check out later***##
    # coefficients = coef(lmA)
    # 
    # # Create a string with the equation
    # eq = paste("y =", round(coefficients[1], 4),"x", "+", round(coefficients[2], 4))
    # 
    # # Add the equation to the plot
    # mtext(eq, side = 3, line = 0)
    # 
    dev.off()
    
    
    #cluster B 
    png(pngB)
    plot(clusterB$total.raw.visits, clusterB$total.crimes,
         xlab = "total Number of Raw Visits",
         ylab = "Total Number of Crimes",
         main = titleNameB)
    
    #plot linear regression
    abline(lmB, col = "Blue")
    
    # #print the equation on graph
    # ####***Doesn't look right but I'll check out later***##
    # coefficients = coef(lmB)
    # 
    # # Create a string with the equation
    # eq <- paste("y =", round(coefficients[1], 4),"x", "+", round(coefficients[2], 4))
    # 
    # # Add the equation to the plot
    # mtext(eq, side = 3, line = 0)
    
    dev.off()
    
    
    ###***Add a section to put outputs of slopes of each cluster's lm into a table***
    
    ##****Added code idea, doing this out of curiousity**
    #run a correlation test 
    corrA = cor(clusterA$total.raw.visits, clusterA$total.crimes)
    corrB = cor(clusterB$total.raw.visits,clusterB$total.crimes)
    
    #print results into a table
    
    
  }
  
}

#dun the new function
###****IMPORTANT! Make sure you manually set the directory so the images get saved to the**
###*##****correct file***
preCovid= lmClusteredFunct(clusteredPre.df1)
postCovid = lmClusteredFunct(clusteredPost.df1)


#test correlation between total raw visits and total crimes for each cluster 
preCovidCor = cor(clusteredPre.df1$total.raw.visits, clusteredPre.df1$total.crimes)
preCovidCor
postCovidCor = cor(clusteredPost.df1$total.raw.visits, clusteredPost.df1$total.crimes)
postCovidCor

filtered.df1 = filter(clusteredPre.df1, total.crimes <200)

plot(clusteredPre.df1$total.raw.visits, clusteredPre.df1$total.crimes)
plot(filtered.df1$total.raw.visits, filtered.df1$total.crimes)
