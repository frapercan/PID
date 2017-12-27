# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 01:00:24 2017

@author: xaxi
"""
import numpy as np


class foreground_estimation(object):
    """
    Clase que clasifica en fondo y figura un conjunto de vectores en base a las dos primeras
    coordenadas x e y, y como último elemento del vector una clasificación.
    
    """
    def __init__(self,clusters,image):
        self.clusters = clusters
        self.image = image
        self.pixels_variation = self.get_pixel_variation()
        self. overlapping_scores = self.get_overlapping_score()
        
    
    def predictor(self):
            return np.exp(-(self.pixel_variation + self.overlapping_score))
        
    def get_pixel_variation(self):
        cluster_areas = np.zeros(len(self.clusters))
        for i in range(len(self.clusters)):
            cluster_areas[i] = sum([1  for vector in self.cluster[i] if vector[-1] == i])        
        return (1/cluster_areas) * sum([(x-(np.mean(x)*x))*(y-(np.mean(y)*y)) for x,y in self.clusters[0:2,:]])
    
    def get_overlappping_score(self,border_radius = 5):
        border_points = [(x+radius,y+radius)) for x,y in vector for vector in clusters for radius in range(border_radius) ]
        return 
        
        
        
            
        
