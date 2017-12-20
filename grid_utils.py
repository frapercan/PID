# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""

import numpy as np


def gridear_imagen(img, distancia_pixeles):
    """Aplica un filtro sobre una imagen en forma de malla.

    función que transforma la imagen cogiendo los pixeles
    superpuestos a una supuesta malla con una distancia entre reja y reja:

    Args:
        img (np.array()): la imagen que vamos a modificar.
        distancia_pixeles (int): Distancia entre lineas de pixeles.

    Returns:
        np.array: la imagen modificada.

    """
    imagen_grideada = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not(i % (distancia_pixeles + 1) == 0 or j % (distancia_pixeles + 1) == 0):
                imagen_grideada[i][j] = [0, 0, 0]
    return imagen_grideada
            
def extrae_puntos_grid_imagen(img, distancia_pixeles):
    """Devuelve un conjunto reducido de los pixeles.

    Aplicando un filtro en forma de malla con una distancia dada, se seleccionan 
    un conjunto de pixeles:

    Args:
        img (np.array()): la imagen que vamos a modificar.
        distancia_pixeles (int): Distancia entre lineas de pixeles.

    Returns:
        list(coordenada_x,coordenada_y,list(Canales_de_color)): 
            la posición de cada uno de los pixeles junto con los valores
            del color correspondiente a su formato. (RGB, LAB, HSV).    
            
    """
    LISTA_PUNTOS =  list([])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (i % distancia_pixeles == 0 or j % distancia_pixeles == 0):
                LISTA_PUNTOS.append([i,j,img[i][j][0],img[i][j][1],img[i][j][2]])
    return np.array(LISTA_PUNTOS)












