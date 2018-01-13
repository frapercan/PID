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
from sklearn.preprocessing import normalize
from scipy.cluster.vq import kmeans,vq,whiten
import numpy as np


class foreground_estimation(object):
    """
    Clase que clasifica en fondo y figura un conjunto de vectores en base a las dos primeras
    coordenadas x e y, y como último elemento del vector una clasificación.

    """

    def __init__(self,x_y_c,image=0):
        self.x_y_c = x_y_c
        self.numero_clusteres = max(x_y_c, key = lambda x: x[-1])[-1]+1
        self.image = image
        #self.pixels_variation = self.get_pixel_variation()
        #self.overlapping_scores = self.get_overlapping_score()


    def classify_points(self):
        fe_scores = self.predictor()
        normalizacion = whiten(fe_scores)
        normalizacion = normalizacion.reshape(-1,1)
        
        centroides,_ = kmeans(normalizacion,k_or_guess=2)
        clases,_ = vq(fe_scores.reshape(-1,1),centroides)
        lista = [[x,y,clases[c]] for x,y,c in self.x_y_c]
        return lista

    def predictor(self):
        return np.exp(-(self.get_pixel_variation() + self.get_overlapping_score()))

    def get_pixel_variation(self):

        cluster_areas = np.zeros(self.numero_clusteres)
        for i in range(self.numero_clusteres):
            cluster_areas[i] = sum([1 for _,_,c in self.x_y_c if c == i])
        #Normalizacion hecho con Normalize. Da valores entre 0 y 1, pero no da valores ni cero ni uno.
        return normalize((1/cluster_areas) * sum([(x-(np.mean(x)*x))*(y-(np.mean(y)*y)) for x,y in self.x_y_c[:,0:2]]))

    def get_overlapping_score(self,border_radius = 5):
        border_points = [(x+radius,y+radius) for x,y,_ in self.x_y_c for radius in range(border_radius)]
        border_points_area = sum([1 for _ in border_points])
        overlapping_points = np.zeros(self.numero_clusteres,dtype=object)
        overlapping_points_area = np.zeros(self.numero_clusteres)
        for i in range(self.numero_clusteres):
            overlapping_points[i] = [(x,y) for x,y,c in self.x_y_c if ((x,y) in border_points and c == i)]
            overlapping_points_area[i] = sum([1 for _ in overlapping_points[i]])
        return overlapping_points_area/border_points_area

          
        
def cambia_formato(mean_shift_result):
    puntos = mean_shift_result.original_points
    clusters = mean_shift_result.cluster_ids
    resultado = np.concatenate((puntos[:,0:2],np.array([clusters]).T),axis=1)
    return resultado






def busca_puntos_cluster_i(i,lista_puntos,clasificacion,rango):
    lista_clasificacion = [c.tolist() for c in clasificacion]
    indices_i = [j for j,x in enumerate(lista_clasificacion) if x == i]
    puntos_cluster_i = [lista_puntos[j] for j in indices_i]
    return puntos_cluster_i

"""
    def variacion_coordenadas_pixeles(lista_puntos,clasificacion):
        pass
    def coste_solapamiento(lista_puntos,clasificacion,rango):
        pass

    vi = variacion_coordenadas_pixeles(lista_puntos,clasificacion)
    bi = coste_solapamiento(lista_puntos,clasificacion,rango)

    fei = math.exp(-(vi+bi))

def foreground_estimation(lista_puntos,clasificacion,rango):
    puntos_visitados = []
    maximo = np.amax(clasificacion)
    for i in range(0,maximo):
        foreground_estimation_i(i,lista_puntos,clasificacion,rango)
uso -> ejecutrar main_prueba y despues foreground_estimation_i(2,mean_shift_result.original_points,mean_shift_result.cluster_ids,3)
"""
