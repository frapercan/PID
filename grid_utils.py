# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""

import numpy as np


def gridear_imagen(img, divisiones):
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
    alto = img.shape[0]
    ancho = img.shape[1]
    for i in range(img.shape[0]):
        if ((i % divisiones) == 0) and ( i != 0)  and ( i != alto ):
            imagen_grideada[i] = np.zeros([ancho,3])
    for j in range(img.shape[1]):
        if (j % divisiones == 0) and (j != 0) and (j != ancho):
            imagen_grideada[:,j] = np.zeros([alto,3])    
    
    return imagen_grideada
            
def extrae_puntos_grid_imagen(img, divisiones):
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
    alto = img.shape[0]
    ancho = img.shape[1]
    for i in range(alto):
        for j in range(ancho):
            if ((i % divisiones == 0) or (j % divisiones == 0)) and (i != 0) and (j != 0) and (i != alto)  and (j != ancho):
                LISTA_PUNTOS.append([i,j,img[i][j][0],img[i][j][1],img[i][j][2]])
    return np.array(LISTA_PUNTOS)

  
def visualizar_clusteres(imagen_original,mean_shift_result):
    """Devuelve un array con la imagen clusterizada.

    Esta imagen tendrá tantos colores como clusteres haya detectado el resultado
    del algoritmo MeanShift pasado por parametro

    Args:
        imagen_original: El array de la imagen original antes de aplicarle el 
        algoritmo de mallado
        mean_shift_result: Resultado del mean_shift aplicado a la imagen original

    Returns:
           Un array de la imagen que da como resultado el mallado coloreado con los diferentes clusters.
            
    """
    shape = np.shape(imagen_original)
    clases = {}
    resultado = np.zeros((shape),dtype='uint8')
    resultado.flags.writeable = True
    puntos_originales = list(mean_shift_result.original_points)
    for (i,j) in list(enumerate(mean_shift_result.cluster_ids)):
        if not (j in clases):
            clases.update({j:[puntos_originales[i][2],puntos_originales[i][3],puntos_originales[i][4]]})
        else:
            color = clases.get(j)
            resultado[puntos_originales[i][0],puntos_originales[i][1]]= color
    return resultado








