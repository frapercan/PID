# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""

"""
Clase de prueba Energy Generation
"""


import PIL
from PIL import Image, ImageFilter
from skimage import io, color,filters
import numpy as np
import random
import energy_generation

#Funcion auxiliar mientras no esta el k means. Sirve para aleatorizar los puntos de figura y de fondo
def cambia_clase(array):
    for i in range(np.shape(array)[0]):
        eleccion = random.choice([0,1])
        array[i,2] = eleccion
#Funcion auxiliar mientras no esta el k means. Sirve para poner los primeros n puntos como puntos de figura.
def cambia_clase_n_primeros(array,n):
    for i in range(np.shape(array)[0]):
        if (i<n):
            array[i,2] = 1
        else:
            array[i,2] = 0
    
##Imagen de muestra en el mismo directorio del archivo
RGB = np.array(io.imread("balloon.jpg"))

import foreground_estimation

import grid_utils as grid
#Extraer los puntos de la imagen que tienen intersección con el Grid
#ORIGINALMENTE ERAN 100
maxsize = (200, 200)

LISTA_PUNTOS = grid.puntos_interseccion(RGB, 10)
print(np.shape(RGB))
print("Numero de puntos: {}".format(len(LISTA_PUNTOS)))
import mean_shift_epanechnikov as ms
#Utilizar el algoritmo meanshift sobre la lista de puntos. 5 Dimensiones + 1 de la clasificación
mean_shifter = ms.MeanShift(kernel = 'epanechnikov_kernel')
#ORIGINALMENTE ERA [0.2,0.2]
mean_shift_result = mean_shifter.cluster(LISTA_PUNTOS, kernel_bandwidth = [400,10])

# Muestra las asignaciones de cada uno de los puntos
cluster_assignments = mean_shift_result.cluster_ids
print(cluster_assignments)
print(mean_shift_result.original_points)
print("Puntos asignados: {}".format(len(cluster_assignments)))

res = grid.visualizar_clusteres(RGB,mean_shift_result)

img = Image.fromarray(res,'RGB')
img.save('cluster_balloon.png','png')


x_y_c = foreground_estimation.cambia_formato(mean_shift_result)
print(x_y_c)
#cambia_clase_n_primeros(x_y_c,20)
cambia_clase(x_y_c)
print(x_y_c)
eg = energy_generation.energy_generation(x_y_c,(65, 100),10)
eg.hacer_saliency_map()
