# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 00:51:40 2017

"""


"""

FEi(vi,bi) = exp(-(vi+bi)), i pertenece a {i,..,k}

vi(ci) = 1/h^d_ci sum[(x,y) pertenece a ci]{ (x-mu*x)*(y-mu*y)}, i pertenece a {i,..,k}

bi(ci,Br) = (h^d_ci pertence a Br)/(h^d_Br), i pertenece a {i,..,k}

"""

import math


import numpy as np


class foreground_estimation(object):
    """
    Clase que clasifica en fondo y figura un conjunto de vectores en base a las dos primeras
    coordenadas x e y, y como último elemento del vector una clasificación.
    
    """
    def __init__(self,clusters,image):
        self.clusters = clusters
        self.image = image
        self.cluster_areas = self.get_cluster_areas()
        self.pixels_variation = self.get_pixel_variation()
        self.overlapping_scores = self.get_overlapping_score()
        
    
    def predictor(self):
        return np.exp(-(self.pixel_variation + self.overlapping_score))
        
    def get_pixel_variation(self):
        cluster_areas = np.zeros(len(self.clusters))
        for i in range(len(self.clusters)):
            cluster_areas[i] = sum([1  for vector in self.cluster[i] if vector[-1] == i])        
        return (1/cluster_areas) * sum([(x-(np.mean(x)*x))*(y-(np.mean(y)*y)) for x,y in self.clusters[0:2,:]])
    
    def get_overlapping_score(self,border_radius = 5):
        border_points = [(x+radius,y+radius) for x,y in vector for vector in self.clusters for radius in range(border_radius)]
        border_points_area = [1 for _ in border_points]
        overlapping_points = np.zeros(len(self.clusters))
        for i in range(len(self.clusters)):
            overlapping_points[i] = [(x,y) for x,y in vector for vector in self.clusters[i] if (x,y) in border_points]  
            overlapping_points_area[i] = sum([1  for vector in overlapping_points[i]])
        return overlapping_points_area[i]/border_points_area

"""

def foreground_estimation_i(i,lista_puntos,clasificacion,rango):
    lista_clasificacion = [c.tolist() for c in clasificacion]
    indices_i = [j for j,x in enumerate(lista_clasificacion) if x == i]
    puntos_cluster_i = [lista_puntos[j] for j in indices_i]
    return puntos_cluster_i
"""
"""    
    def variacion_coordenadas_pixeles(lista_puntos,clasificacion):
        
        pass
    def coste_solapamiento(lista_puntos,clasificacion,rango):
        pass
    
    vi = variacion_coordenadas_pixeles(lista_puntos,clasificacion)
    bi = coste_solapamiento(lista_puntos,clasificacion,rango)
    
    fei = math.exp(-(vi+bi))
"""        
"""   
def foreground_estimation(lista_puntos,clasificacion,rango):
    puntos_visitados = []
    maximo = np.amax(clasificacion)
    for i in range(0,maximo):
        foreground_estimation_i(i,lista_puntos,clasificacion,rango)
    
        
uso -> ejecutrar main_prueba y despues foreground_estimation_i(2,mean_shift_result.original_points,mean_shift_result.cluster_ids,3)
"""