'''
Created on Jun 4, 2018

@author: Sam
'''
import matplotlib.pyplot as plt
import datetime as datetime
from constants import OUTPUT_DIR
from mpl_toolkits.mplot3d import Axes3D


class PredictorsPlot:

    def __init__(self, filename=OUTPUT_DIR+datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")):

        self._filename = filename
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(111, projection='3d')

        self._colors()

    def plot_training_data(self, list_of_predictors, list_of_responses):
        """Assumes the category responses are either of the form (A, B, C,...) or (0, 1, 2...)"""
        for i in range(len(list_of_predictors)):
            self.plot_point(list_of_predictors[i][0], list_of_predictors[i][1], list_of_predictors[i][2], list_of_responses[i], 'o')

    def plot_testing_data(self, list_of_predictors, list_of_responses):
        """Assumes the category responses are either of the form (A, B, C,...) or (0, 1, 2...)"""
        for i in range(len(list_of_predictors)):
            self.plot_point(list_of_predictors[i][0], list_of_predictors[i][1], list_of_predictors[i][2], list_of_responses[i], '+')

    def plot_point(self, x, y, z, category, marker):
        """Assumes the category responses are either of the form (A, B, C,...) or (0, 1, 2...)"""
        self._ax.scatter(x, y, z, c=self._colors[category], marker=marker)

    def show(self):
        plt.show()

    def __enter__(self):
        # Method in place for the WITH keyword
        return self

    def __exit__(self, *args):
        self._ax.set_xlabel('Predictor 1')
        self._ax.set_ylabel('Predictor 2')
        self._ax.set_zlabel('Predictor 3')
        self._fig.savefig(self._filename)

    def _colors(self):
        self._colors = {None: "black",
                        "A": 'tab:blue',
                        "B": 'tab:orange',
                        "C": 'tab:green',
                        "D": 'tab:red',
                        "E": 'tab:purple',
                        "F": 'tab:brown',
                        "G": 'tab:pink',
                        "H": 'tab:gray',
                        "I": 'tab:olive',
                        "J": 'tab:cyan',
                        "K": 'C0',
                        "L": 'C1',
                        "M": 'C2',
                        "N": 'C3',
                        "O": 'C4',
                        "P": 'C5',
                        "Q": 'C6',
                        "R": 'C7',
                        "S": 'C8',
                        "T": 'C9',
                        0: 'tab:blue',
                        1: 'tab:orange',
                        2: 'tab:green',
                        3: 'tab:red',
                        4: 'tab:purple',
                        5: 'tab:brown',
                        6: 'tab:pink',
                        7: 'tab:gray',
                        8: 'tab:olive',
                        9: 'tab:cyan',
                        10: 'C0',
                        11: 'C1',
                        12: 'C2',
                        13: 'C3',
                        14: 'C4',
                        15: 'C5',
                        16: 'C6',
                        17: 'C7',
                        18: 'C8',
                        19: 'C9'
                        }
