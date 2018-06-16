library("ggplot2")
library("ggthemes")
library("RColorBrewer")
library("gridExtra")
library("grid")
###############################################
# Helper Functions; Start Coding at ~Line 60
###############################################

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

two_dim <- function(class_column, target_column, data_frame){
  to_return <- data.frame(X=numeric(), Y=numeric(), Class=character())
  X <- c()
  Y <- c()
  Class <- c()
  
  for(i in 1:nrow(data_frame)){
    for(j in 1:ncol(data_frame)){
      #row <- c(target_column[i], data_frame[i,j], paste(class_column[i]))
      X <- c(X, target_column[i])
      Y <- c(Y, data_frame[i,j])
      Class <- c(Class, paste(class_column[i]))
    }
  }
  to_return <- data.frame(X, Y, Class)
  colnames(to_return)<-c("X", "Y", "Class")
  return(to_return)
}

manual_trend <- function(x){
  return(0.003931514469-0.007841398074*x+0.003909913358*x*x)
  #return(x*0.06253-0.06270)
}

manual_trend_sum <- function(x){
  return(0.3543454+1.0341490*x+0.2406895*x*x)
  #return(x*0.06253-0.06270)
}

plot_fit_time<-function(all_data){
  labels_individual <- (c("Individual Classifer Training Instance\n", "\nFitted Quadratic Model\n--------------------------------\n P-value: < 2.2e-16;\n Adjusted R-squared: 0.9775"))
  
  d22 <- two_dim(all_data$Method, all_data$NumberOfTrainingObservations, get_fit_time(all_data))
  color_plate <- c("#4E79A7", "#F28E2C")
  
  p <- ggplot()
  p <- p + scale_colour_manual(labels=labels_individual, values = (color_plate), guide = guide_legend(override.aes = list( linetype = (c("blank", "solid")), shape = (c(16, NA)))))
  p <- p + geom_point(aes(x=d22$X, y=d22$Y, colour="A"), size=1)
  #p <- p + geom_smooth(aes(formula=d22$Y~poly(d22$X, 2), colour ="-"), method='lm')
  p <- p + stat_function(fun=manual_trend, aes(color="B"))
  p <- p + labs(x=NULL, y="Time to Train\n(Seconds)",title = "Predicting Isomorphism Class - Training Times Overview", subtitle=paste("Prediction Dataset Used:", all_data$PredictorSet[1]), col=NULL)
  p <- p + theme_bw() + theme(legend.position = c(0.2, 0.7),legend.title = element_blank(), legend.background = element_rect(size=0.5, linetype="solid", 
                                                                                                                              colour ="black"))
  print(p)
  return(p)
}

plot_fit_time_sum<-function(all_data){
  labels_sum <- c("Aggregated Classifier Training Times\n", "Fitted Quadratic Model\n--------------------------------\n P-value: 1.979e-09;\n Adjusted R-squared: 0.9858")
  d22 <- two_dim(all_data$Method, all_data$NumberOfTrainingObservations, get_fit_time(all_data))
  d22_sum <- aggregate(d22$Y , by=list(d22$X), sum)
  
  color_plate <- c("#76B7B2", "#E15759")
  
  p <- ggplot()
  p <- p + scale_colour_manual(labels = labels_sum, values = color_plate, guide = guide_legend(override.aes = list( linetype = c("blank", "solid"), shape = c(16, NA))))
  p <- p + geom_point(aes(x=d22_sum$Group.1, y=d22_sum$x, colour="A"), size=1)
  #p <- p + geom_smooth(aes(formula=d22$Y~poly(d22$X, 2), colour ="-"), method='lm')
  p <- p + stat_function(fun=manual_trend_sum, aes(color="B"))
  p <- p + labs(x="Number Of Tournaments Used For Training", y="Cummulative Time to Train All Classifiers\n(With 10-Fold Validation) (Seconds)", title = NULL, subtitle=NULL, col=NULL)
  p <- p + theme_bw() +theme(legend.position = c(0.2, 0.7),legend.title = element_blank(), legend.background = element_rect(size=0.5, linetype="solid", 
                                                                                                                             colour ="black"))
  
  print(p)
  return(p)
}

all_data <- read.csv("../output/T4-Adj-Numbers.csv")

p1 <- plot_fit_time(all_data)
p2 <- plot_fit_time_sum(all_data)

gA<-ggplot_gtable(ggplot_build(p1))
gB<-ggplot_gtable(ggplot_build(p2))

maxWidth = grid::unit.pmax(gA$widths[2:3], gB$widths[2:3])
gA$widths[2:3] <- as.list(maxWidth)
gB$widths[2:3] <- as.list(maxWidth)

grid.newpage()
grid.arrange(arrangeGrob(gA,gB,nrow=2,heights=c(.5,.5)))


