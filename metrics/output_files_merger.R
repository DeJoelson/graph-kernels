get_fit_time <- function(data_frame){
  to_return <- data.frame(data_frame$FitTime0, data_frame$FitTime1, data_frame$FitTime2, data_frame$FitTime3, data_frame$FitTime4, data_frame$FitTime5, data_frame$FitTime6, data_frame$FitTime7, data_frame$FitTime8, data_frame$FitTime9)
  return(to_return)
}
get_score_time <- function(data_frame){
  to_return <- data.frame(data_frame$ScoreTime0, data_frame$ScoreTime1, data_frame$ScoreTime2, data_frame$ScoreTime3, data_frame$ScoreTime4, data_frame$ScoreTime5, data_frame$ScoreTime6, data_frame$ScoreTime7, data_frame$ScoreTime8, data_frame$ScoreTime9)
  return(to_return)
}
get_train_accuracy <- function(data_frame){
  to_return <- data.frame(data_frame$TrainAccuracy0, data_frame$TrainAccuracy1, data_frame$TrainAccuracy2, data_frame$TrainAccuracy3, data_frame$TrainAccuracy4, data_frame$TrainAccuracy5, data_frame$TrainAccuracy6, data_frame$TrainAccuracy7, data_frame$TrainAccuracy8, data_frame$TrainAccuracy9)
  return(to_return)
}
get_test_accuracy <- function(data_frame){
  to_return <- data.frame(data_frame$TestAccuracy0, data_frame$TestAccuracy1, data_frame$TestAccuracy2, data_frame$TestAccuracy3, data_frame$TestAccuracy4, data_frame$TestAccuracy5, data_frame$TestAccuracy6, data_frame$TestAccuracy7, data_frame$TestAccuracy8, data_frame$TestAccuracy9)
  return(to_return)
}

merge_files <- function(ratioCSV, numbersCSV){
  
  ratioCSV$PercentageOfDataUsedForTraining <- 1 - ratioCSV$TestingTrainingSeperationRatio
  
  ratioCSV$TestingTrainingSeperationRatio <- NULL
  
  ratioCSV$NumberOfTrainingObservations <- floor(ratioCSV$PercentageOfDataUsedForTraining * ratioCSV$TotalObservations)
  
  numbersCSV$PercentageOfDataUsedForTraining <- numbersCSV$NumberOfTrainingObservations/numbersCSV$TotalObservations
  
  merged <- rbind(ratioCSV, numbersCSV)
  
  merged$MedianTrainingTime <- apply(get_fit_time(merged), 1, median)
  
  merged$TrainingDataAccuracyMean <- apply(get_train_accuracy(merged), 1, mean)
  merged$TrainingDataAccuracyStandardDeviation <- apply(get_train_accuracy(merged), 1, sd)
  
  merged$TestDataAccuracyMean <- apply(get_test_accuracy(merged), 1, mean)
  merged$estDataAccuracyStandardDeviation <- apply(get_test_accuracy(merged), 1, sd)
  
  merged[,c(-1,-2,-3)] <- round(merged[,c(-1,-2,-3)], 4)
  
  merged$TestingTrainingSeperationRatio <- NULL
  
  merged$FitTime0 <- NULL
  merged$FitTime1 <- NULL
  merged$FitTime2 <- NULL
  merged$FitTime3 <- NULL
  merged$FitTime4 <- NULL
  merged$FitTime5 <- NULL
  merged$FitTime6 <- NULL
  merged$FitTime7 <- NULL
  merged$FitTime8 <- NULL
  merged$FitTime9 <- NULL
  
  merged$ScoreTime0 <- NULL
  merged$ScoreTime1 <- NULL
  merged$ScoreTime2 <- NULL
  merged$ScoreTime3 <- NULL
  merged$ScoreTime4 <- NULL
  merged$ScoreTime5 <- NULL
  merged$ScoreTime6 <- NULL
  merged$ScoreTime7 <- NULL
  merged$ScoreTime8 <- NULL
  merged$ScoreTime9 <- NULL
  
  merged$TrainAccuracy0 <- NULL
  merged$TrainAccuracy1 <- NULL
  merged$TrainAccuracy2 <- NULL
  merged$TrainAccuracy3 <- NULL
  merged$TrainAccuracy4 <- NULL
  merged$TrainAccuracy5 <- NULL
  merged$TrainAccuracy6 <- NULL
  merged$TrainAccuracy7 <- NULL
  merged$TrainAccuracy8 <- NULL
  merged$TrainAccuracy9 <- NULL
  
  merged$TestAccuracy0 <- NULL
  merged$TestAccuracy1 <- NULL
  merged$TestAccuracy2 <- NULL
  merged$TestAccuracy3 <- NULL
  merged$TestAccuracy4 <- NULL
  merged$TestAccuracy5 <- NULL
  merged$TestAccuracy6 <- NULL
  merged$TestAccuracy7 <- NULL
  merged$TestAccuracy8 <- NULL
  merged$TestAccuracy9 <- NULL
  
  return(merged)
}

dataSet <- "T4-AdjacencyMatrix"

ratioData <- read.csv(paste(dataSet, "-Ratio.csv", sep=""))
numberData <- read.csv(paste(dataSet, "-Numbers.csv", sep=""))

m <- m <- merge_files(ratioData, numberData)

plot(m$PercentageOfDataUsedForTraining, m$TestDataAccuracyMean, col=m$Method, pch=16, main=dataSet)
