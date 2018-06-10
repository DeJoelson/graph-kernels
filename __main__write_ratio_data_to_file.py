'''
Created on May 30, 2018

@author: Sam
'''

import random
from constants import OUTPUT_DIR, RANDOM_SEED
from metrics.evaluator import Evaluator
import datetime

import data.T4_Lap as dta

if __name__ == '__main__':
    
    data = dta.get_T4_Lap()
    data_format = "LaplacianMatrix"
    TOrder = "T4"

    X = []
    y = [] 
    
    random.seed(RANDOM_SEED)
    random.shuffle(data)
    
    for item in data:
        X.append(item[1])
        y.append(item[0])

    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()

    for i in range(0,17):
        test_size_ratio = 1 - ((i*5+10)/100)
        print(i, "Of 17")

        evaluator_device = Evaluator(X, y)
        evaluator_device.cross_validate_to_file(file_name=OUTPUT_DIR+TOrder+"-"+data_format+"-Ratio.csv", predictor_set_name=TOrder+"-"+data_format,test_size_ratio=test_size_ratio)

        print("Total Time Last: ", datetime.datetime.now()-endTime)
        endTime = datetime.datetime.now()
        print("Total Time Spent: ", endTime-startTime)
