'''
Created on Jun 4, 2018

@author: Sam
'''
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from constants import RANDOM_SEED, RANDOM_FOREST_DEFAULT_TREE_COUNT
import math as math


class Evaluator(object):

    def __init__(self, all_predictor_variables, all_response_variables):
        self._all_predictor_variables = all_predictor_variables
        self._all_response_variables = all_response_variables

    def cross_validate(self, test_size, classifiers=None):
        if classifiers is None:
            number_of_total_observations = len(self._all_predictor_variables)
            number_of_training_observations = number_of_total_observations - int(number_of_total_observations * test_size)
            classifiers = self.get_default_classifiers(number_of_training_observations)

    @staticmethod
    def get_default_classifiers(self, number_of_training_observations):
        sqrt_obs = int(math.sqrt(number_of_training_observations))
        classifiers = []
        classifiers.append(KNeighborsClassifier(1))  # k-nn, with k=1
        classifiers.append(KNeighborsClassifier(sqrt_obs))  # k-nn, with k=sqrt(number of training observations)
        classifiers.append(GaussianNB())  # Gaussian Naive Bayes
        classifiers.append(SVC(kernel="linear", random_state=RANDOM_SEED))  # Support Vector Machine with Linear Kernel
        classifiers.append(SVC(kernel="rbf", random_state=RANDOM_SEED))  # Support Vector Machine with Radial Basis Kernel
        classifiers.append(DecisionTreeClassifier(random_state=RANDOM_SEED))  # Single Decision Tree
        classifiers.append(RandomForestClassifier(n_estimators=RANDOM_FOREST_DEFAULT_TREE_COUNT, random_state=RANDOM_SEED))  # Random Forest

        return classifiers
