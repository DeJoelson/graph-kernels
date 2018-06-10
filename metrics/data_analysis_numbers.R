library("ggplot2")
library("ggthemes")
library("RColorBrewer")
library("gridExtra")
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

two_dim <- function(target_column, data_frame){
  to_return <- data.frame(response=numeric(), predictor=numeric())
  for(i in 1:nrow(data_frame)){
    for(j in 1:ncol(data_frame)){
      to_return <- rbind(to_return, c(target_column[i], data_frame[i,j]))
    }
  }
  colnames(to_return)<-c("Response", "Predictor")
  return(to_return)
}





plot_accuracy<-function(plotting_data){
  
  data_train <- two_dim(plotting_data$NumberOfTrainingObservations, get_train_accuracy(plotting_data))
  data_test <- two_dim(plotting_data$NumberOfTrainingObservations, get_test_accuracy(plotting_data))
  
  q_test_mean <- aggregate(data_test$Predictor , by=list(data_test$Response), mean)
  q_test_sd <- aggregate(data_test$Predictor , by=list(data_test$Response), sd)
  q_train_mean <- aggregate(data_train$Predictor , by=list(data_train$Response), mean)
  q_train_sd <- aggregate(data_train$Predictor , by=list(data_train$Response), sd)
  
  color_plate <- c("#4E79A7", "#F28E2C")
  p <- ggplot() +
    scale_colour_manual(values = color_plate, labels = c("Training Data", "Testing Data"), guide = guide_legend(override.aes = list(
      linetype = c("dashed", "solid"),
      shape = c(17, 16)))) +
    
    geom_line(aes(x=q_train_mean$Group.1, y=q_train_mean$x*100, colour=color_plate[1]), se=FALSE, linetype="dashed") +
    geom_point(aes(x=q_train_mean$Group.1, y=q_train_mean$x*100, colour=color_plate[1]), shape=17, size=1) +
    
    geom_line(aes(x=q_test_mean$Group.1, y=q_test_mean$x*100, colour=color_plate[2]), se=FALSE) +
    geom_point(aes(x=q_test_mean$Group.1, y=q_test_mean$x*100, colour=color_plate[2]), shape=16, size=2) +

    ylim(0, 100)+
    labs(x=NULL, y="10-Fold Validation:\nMean Accuracy (%)", title = "Predicting Isomorphism Class", subtitle=paste(" Prediction Dataset Used:", plotting_data$PredictorSet[1], "\n","Final Classification Method Used:", plotting_data$Method[1]), col=NULL) +
    theme_bw() + theme(legend.position = c(0.88, 0.2),legend.title = element_blank(), legend.background = element_rect(size=0.5, linetype="solid", 
                                                                                       colour ="black"))
  #print(p)
  return(p)
}

p1 <- plot_accuracy(plotting_data)

plot_fit_time<-function(plotting_data){
  d2 <- two_dim(plotting_data$NumberOfTrainingObservations, get_fit_time(plotting_data))
  
  
  q_time <- aggregate(d2$Predictor , by=list(d2$Response), mean)
  q_sd <- aggregate(d2$Predictor , by=list(d2$Response), sd)
  
  color_plate <- c("#E15759")
  p <- ggplot() +
    scale_colour_manual(values = color_plate, labels = (c("Time", "LOESS Trendline \n (95% Conf. Interval)"))) +
    
    geom_line(aes(x=q_time$Group.1, y=q_time$x, colour=color_plate[1]), se=FALSE) +
    geom_point(aes(x=q_time$Group.1, y=q_time$x, colour=color_plate[1]), shape=16, size=2) +
    
    labs(x="Number Of Graphs Used For Training", y="Median Time to Train\n(Seconds)", title = NULL, subtitle=NULL, col=NULL) +
    theme_bw() + theme(legend.position="none")
  #print(p)
  return(p)
}
p2 <- plot_fit_time(plotting_data)



###############################################
# Plot Stuff Here
###############################################




method = "SVM-LinearKernel"
t4 <- read.csv("../output/T4-Adj-Numbers.csv")

plotting_data=t4[t4$Method==method,]

p1 <- plot_accuracy(plotting_data)
p2 <- plot_fit_time(plotting_data)

gA<-ggplot_gtable(ggplot_build(p1))
gB<-ggplot_gtable(ggplot_build(p2))
maxWidth = grid::unit.pmax(gA$widths[2:3], gB$widths[2:3])
gA$widths[2:3] <- as.list(maxWidth)
gB$widths[2:3] <- as.list(maxWidth)

grid.newpage()
grid.arrange(arrangeGrob(gA,gB,nrow=2,heights=c(.666,.333)))


for(method in unique(t4$Method)){
  filename <- paste('../output/plotT4AdjIso',method,"-Number.pdf", sep="")
  plotting_data=t4[t4$Method==method,]

  pdf(filename, width=6, height=4 )

  p1 <- plot_accuracy(plotting_data)
  p2 <- plot_fit_time(plotting_data)
  
  gA<-ggplot_gtable(ggplot_build(p1))
  gB<-ggplot_gtable(ggplot_build(p2))
  maxWidth = grid::unit.pmax(gA$widths[2:3], gB$widths[2:3])
  gA$widths[2:3] <- as.list(maxWidth)
  gB$widths[2:3] <- as.list(maxWidth)
  

  grid.arrange(arrangeGrob(gA,gB,nrow=2,heights=c(.666,.333)))

  dev.off()
}
