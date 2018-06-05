from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier
from technique.schwartz_predictor_converter import SchwartzPredictorConverter

class SchwartzClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, last_step_classifier=None, schwartz_predictor_converter=None):
        self._fit_already_called = False
        self._schwartz_predictor_converter = schwartz_predictor_converter
        
        if last_step_classifier is None:
            self.last_step_classifier = KNeighborsClassifier(1)
        else:
            self.last_step_classifier = last_step_classifier

    def fit(self, X, y=None):
        if self._fit_already_called is True:
            raise AssertionError("Fit already called")
        
        self._fit_already_called = True

        if self._schwartz_predictor_converter is None:
            self._schwartz_predictor_converter = SchwartzPredictorConverter(X)

        convertedX = self._schwartz_predictor_converter.convert_predictors(X)

        self.last_step_classifier.fit(convertedX, y)

    def predict(self, X):
        convertedX = self._schwartz_predictor_converter.convert_predictors(X)
        return self.last_step_classifier.predict(convertedX)
