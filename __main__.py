'''
Created on May 30, 2018

@author: Sam
'''
from metrics.predictors_plot import PredictorsPlot
import data.pre_canned_data as pcd
import numpy.random as random
from technique.schwartz_classifier import SchwartzClassifier
from random import shuffle
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import GaussianNB
from constants import RANDOM_SEED, OUTPUT_DIR
from metrics.evaluator import Evaluator
import sys
import datetime
import time

if __name__ == '__main__':

    X = []
    y = [] 
    data = pcd.get_data2()
    shuffle(data)
    for item in data:
        X.append(item[1])
        y.append(item[0])
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    for i in range(0,17):
        test_size_ratio = 1 - ((i*5+10)/100)
        print(i, "Of 17")

        evaluator_device = Evaluator(X, y)
        evaluator_device.cross_validate_to_file(file_name=OUTPUT_DIR+"T5-Adj.csv", predictor_set_name="T5-Adj",test_size_ratio=test_size_ratio)

        print("Total Time Last: ", datetime.datetime.now()-endTime)
        endTime = datetime.datetime.now()
        print("Total Time Spent: ", endTime-startTime)
