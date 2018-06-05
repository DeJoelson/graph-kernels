'''
Created on Jun 4, 2018

@author: Sam
'''
from technique import jensen_shannon_divergence_kernel as jsdk
import numpy as np
from sklearn.decomposition import PCA


class SchwartzPredictorConverter:

    
    def __init__(self, training_data):
        
        self._training_data = training_data
        
        kernal_matrix = jsdk.get_kernel_matrix(self._training_data)
     
        # Run Principal Component Analysis on kernel matrix
        pca = PCA()
        pca.fit(kernal_matrix)
        
        self._pca_components = pca.components_
    
    
    def convert_predictor(self, individual_predictor):
        x = []
        for training_instance in self._training_data:
            x.append(jsdk.get_jensen_shannon_diffusion_kernel(training_instance, individual_predictor))
        
        to_return = []
        for component in self._pca_components:
            to_return.append(np.dot(component, x))
        
        return to_return
       
    def convert_predictors(self, list_of_predictors):
        return [self.convert_predictor(individual_predictor) for individual_predictor in list_of_predictors] 