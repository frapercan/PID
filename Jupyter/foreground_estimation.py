# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 00:51:40 2017

"""


import math
from sklearn.preprocessing import normalize
from scipy.cluster.vq import kmeans,vq,whiten
import numpy as np

"""
Clase que clasifica en fondo y figura un conjunto de vectores en base a las dos primeras
coordenadas x e y, y como último elemento del vector una clasificación.

"""


class foreground_estimation(object):
    """
    Constructor
    x_y_c: Lista de puntos aislados con la información (x,y,c). Siendo x la posición x, y la posición y, y c el cluster al que pertenece.
    numero_clusteres: numero de clusteres
    """
    def __init__(self,x_y_c):
        self.x_y_c = x_y_c
        self.numero_clusteres = max(x_y_c, key = lambda x: x[-1])[-1]+1


    """
    Función que clasifica los puntos segun si son fondo o figura con k-means.
    """
    def classify_points(self):
        fe_scores = self.predictor()
        normalizacion = whiten(fe_scores)
        normalizacion = normalizacion.reshape(-1,1)
        centroides,_ = kmeans(normalizacion,k_or_guess=2,thresh=1e-9)
        centroides = np.sort(centroides,axis=None)
        centroides = [[c] for c in centroides][::-1]
        clases,_ = vq(fe_scores.reshape(-1,1),centroides)
        lista = [[x,y,clases[c]] for x,y,c in self.x_y_c]
        return lista

    """
    Función que calcula el score de pertenencia a fondo o figura de cada cluster.
    """
    def predictor(self):
        return np.exp(-(self.get_pixel_variation() + self.get_overlapping_score()))

    """
    Función que calcula la variación espacial de los pixeles de cada cluster.
    """
    def get_pixel_variation(self):

        cluster_areas = np.zeros(self.numero_clusteres)
        for i in range(self.numero_clusteres):
            cluster_areas[i] = sum([1 for _,_,c in self.x_y_c if c == i])
            
        cluster_areas = cluster_areas.reshape(1,-1)
        #Normalizacion hecho con Normalize. Da valores entre 0 y 1, pero no da valores ni cero ni uno.
        return normalize((1/cluster_areas) * sum([(x-(np.mean(x)*x))*(y-(np.mean(y)*y)) for x,y in self.x_y_c[:,0:2]]))

    """
    Función que calcula el score de como la figura esta cerca del centro de la imagen.
    """
    
    def get_overlapping_score(self,border_radius = 5):
        border_points = [(x+radius,y+radius) for x,y,_ in self.x_y_c for radius in range(border_radius)]
        border_points_area = sum([1 for _ in border_points])
        overlapping_points = np.zeros(self.numero_clusteres,dtype=object)
        overlapping_points_area = np.zeros(self.numero_clusteres)
        for i in range(self.numero_clusteres):
            overlapping_points[i] = [(x,y) for x,y,c in self.x_y_c if ((x,y) in border_points and c == i)]
            overlapping_points_area[i] = sum([1 for _ in overlapping_points[i]])
        return overlapping_points_area/border_points_area

          
"""
Función auxiliar que cambia el resultado del meanshift a un resultado como lista de elementos (x,y,c) donde:
    x es la coordenada x
    y la coordenada y
    y c es el cluster que tiene asignado del meanshift
"""  
def cambia_formato(mean_shift_result):
    puntos = mean_shift_result.original_points
    clusters = mean_shift_result.cluster_ids
    resultado = np.concatenate((puntos[:,0:2],np.array([clusters]).T),axis=1)
    return resultado


