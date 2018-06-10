'''
Created on May 30, 2018

@author: Sam
'''

import random
from constants import OUTPUT_DIR, RANDOM_SEED
from metrics.evaluator import Evaluator
import datetime

import data.T5_Adj as dta

if __name__ == '__main__':
    
    data = dta.get_T5_Adj()
    data_format = "AdjacencyMatrix"
    TOrder = "T5"

    X = []
    y = [] 

    random.seed(RANDOM_SEED)
    random.shuffle(data)

    for item in data:
        X.append(item[1])
        y.append(item[0])

    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()

    total_observations = len(X)
    iterations = min(50, int(total_observations/5))

    for i in range(0, iterations):  #Increment by 5 observations
        number_of_training_observations = i*5+5
        print("Working on", TOrder, data_format)
        print(i, "Of ", iterations)

        evaluator_device = Evaluator(X, y)
        evaluator_device.cross_validate_to_file_number_based(file_name=OUTPUT_DIR+TOrder+"-"+data_format+"-Numbers.csv", predictor_set_name=TOrder+"-"+data_format,training_observations=number_of_training_observations)

        print("Total Time Last: ", datetime.datetime.now()-endTime)
        endTime = datetime.datetime.now()
        print("Total Time Spent: ", endTime-startTime)
