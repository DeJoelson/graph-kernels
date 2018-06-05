'''
Created on Jun 4, 2018

@author: Sam
'''
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection as model_selection
from constants import RANDOM_SEED, RANDOM_FOREST_DEFAULT_TREE_COUNT, OUTPUT_DIR
import math as math
import datetime as datetime
import csv
from technique.schwartz_classifier import SchwartzClassifier

class Evaluator(object):

    def __init__(self, all_predictor_variables, all_response_variables):
        self._all_predictor_variables = all_predictor_variables
        self._all_response_variables = all_response_variables
        self._number_of_total_observations = len(self._all_predictor_variables)

    def cross_validate_to_file(self, file_name=None, predictor_set_name=None, test_size_ratio=0.2, classifiers=None):
        if file_name is None:
            file_name = OUTPUT_DIR + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + ".csv";
        if predictor_set_name is None:
            predictor_set_name = "Predictors"
        if classifiers is None:
            number_of_training_observations = self._number_of_total_observations - int(self._number_of_total_observations * test_size_ratio)
            classifiers = self.get_default_classifiers(number_of_training_observations)
        
        classifier_count = len(classifiers)
        for i, classifer in enumerate(classifiers):
            classifer_name = str(type(classifer).__name__)
            print("Working On " + classifer_name + "; #" + str(i) + " of " + str(classifier_count) + "(" + str(i * 100 / classifier_count) + "%); " + "filename: " + file_name)

            schwartz_classifier = SchwartzClassifier(classifer)
            cvout = self._cross_validate_individual_classifier(schwartz_classifier, test_size_ratio)
            
            print("Output: ", cvout)

            self._write_file_line(file_name, predictor_set_name, classifer_name, self._number_of_total_observations, test_size_ratio, cvout)
        
    def _write_file_line(self, file_name, predictor_set_name, method, total_observations, test_size_ratio, cvout):
        with open(file_name, 'a') as csvfile:
            thewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            to_write = [predictor_set_name, method, str(total_observations), str(test_size_ratio)]
            to_write += [str(datum) for datum in cvout['fit_time']]
            to_write += [str(datum) for datum in cvout['score_time']]
            to_write += [str(datum) for datum in cvout['train_score']]
            to_write += [str(datum) for datum in cvout['test_score']]
            thewriter.writerow(to_write)
            
        
    def _cross_validate_individual_classifier(self, classifier, test_size_ratio):
        cv_options = model_selection.ShuffleSplit(n_splits=10, test_size=test_size_ratio, random_state=RANDOM_SEED)
        X = self._all_predictor_variables
        y = self._all_response_variables
        
        out = model_selection.cross_validate(classifier, X, y, scoring="accuracy", cv=cv_options, return_train_score='warn')
        return out

    @staticmethod
    def get_default_classifiers(number_of_training_observations):
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
