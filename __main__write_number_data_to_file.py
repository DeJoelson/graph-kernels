'''
Created on May 30, 2018

@author: Sam
'''

import random
from constants import OUTPUT_DIR, RANDOM_SEED
from metrics.evaluator import Evaluator
import datetime

import data.T6_Adj_FAST_Unlabled as dta

if __name__ == '__main__':
    
    data = dta.get_T6_Adj_FAST_Unlabled()
    data_format = "AdjacencyMatrix-Unlabeled"
    TOrder = "T6"
    is_FAST = True

    X = []
    y = [] 

    random.seed(RANDOM_SEED)
    #random.seed(2)
    random.shuffle(data)

    for item in data:
        X.append(item[1])
        y.append(item[0])

    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()

    total_observations = len(X)
    iterations = min(50, int(total_observations/5))
    
    file_suffix = ""
    
    if is_FAST:
        file_suffix = "-FAST"
        
    filename = OUTPUT_DIR+TOrder+"-"+data_format+file_suffix+"-Numbers.csv"
    
    with open(filename, "a") as f:
        header = "PredictorSet, Method, TotalObservations, NumberOfTrainingObservations, FitTime0, FitTime1, FitTime2, FitTime3, FitTime4, FitTime5, FitTime6, FitTime7, FitTime8, FitTime9, ScoreTime0, ScoreTime1, ScoreTime2, ScoreTime3, ScoreTime4, ScoreTime5, ScoreTime6, ScoreTime7, ScoreTime8, ScoreTime9, TrainAccuracy0, TrainAccuracy1, TrainAccuracy2, TrainAccuracy3, TrainAccuracy4, TrainAccuracy5, TrainAccuracy6, TrainAccuracy7, TrainAccuracy8, TrainAccuracy9, TestAccuracy0, TestAccuracy1, TestAccuracy2, TestAccuracy3, TestAccuracy4, TestAccuracy5, TestAccuracy6, TestAccuracy7, TestAccuracy8, TestAccuracy9"
        f.write(header + "\n")

    for i in range(0, iterations):  #Increment by 5 observations
        number_of_training_observations = i*5+5
        print("Working on", TOrder, data_format)
        print(i, "Of ", iterations)

        evaluator_device = Evaluator(X, y)
        evaluator_device.cross_validate_to_file_number_based(file_name=filename, predictor_set_name=TOrder+"-"+data_format,training_observations=number_of_training_observations)

        print("Total Time Last: ", datetime.datetime.now()-endTime)
        endTime = datetime.datetime.now()
        print("Total Time Spent: ", endTime-startTime)
