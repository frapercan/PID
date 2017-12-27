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


def foreground_estimation_i(i,lista_puntos,clasificacion,rango):
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
    
"""    
    
def foreground_estimation(lista_puntos,clasificacion,rango):
    puntos_visitados = []
    maximo = np.amax(clasificacion)
    for i in range(0,maximo):
        foreground_estimation_i(i,lista_puntos,clasificacion,rango)
    
        

"""

uso -> ejecutrar main_prueba y despues foreground_estimation_i(2,mean_shift_result.original_points,mean_shift_result.cluster_ids,3)
"""