# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""
import PIL
from PIL import Image, ImageFilter
from skimage import io, color,filters
import numpy as np

##Imagen de muestra en el mismo directorio del archivo
RGB = np.array(io.imread("balloon.jpg"))

RGB2 = PIL.Image.open("jakob-nielsen-thumbs-up.jpg")

LAB = np.array(color.rgb2lab(RGB2))

HSV = np.array(color.rgb2hsv(RGB2))

##Aplicamos los filtros gaussianos y almacenamos en variables
GAUSSIAN_KERNELS = [1, 3, 5]

#RGB1 = filters.gaussian(RGB,GAUSSIAN_KERNELS[0])
RGB2 = RGB2.filter(ImageFilter.GaussianBlur(GAUSSIAN_KERNELS[1]))


RGB2.save('blurred.png','png')

#RGB3 = filters.gaussian(RGB,GAUSSIAN_KERNELS[2])
#
#LAB1 = filters.gaussian(LAB,GAUSSIAN_KERNELS[0])
LAB2 = filters.gaussian(LAB,GAUSSIAN_KERNELS[1])
#LAB3 = filters.gaussian(LAB,GAUSSIAN_KERNELS[2])
#
#HSV1 = filters.gaussian(HSV,GAUSSIAN_KERNELS[0])
HSV2 = filters.gaussian(HSV,GAUSSIAN_KERNELS[1])
#HSV3 = filters.gaussian(HSV,GAUSSIAN_KERNELS[2])

import foreground_estimation
import bayesian

import grid_utils as grid
#Extraer los puntos de la imagen que tienen intersección con el Grid
#ORIGINALMENTE ERAN 100
maxsize = (200, 200)

#RGB2.thumbnail(maxsize, PIL.Image.ANTIALIAS)

RGB2 = np.array(RGB2)
print(np.shape(RGB2))
# LISTA_PUNTOS =  list([])
# alto = RGB2.shape[0]
# ancho = RGB2.shape[1]
# for i in range(alto):
#      for j in range(ancho):
#          LISTA_PUNTOS.append([i,j,RGB2[i][j][0],RGB2[i][j][1],RGB2[i][j][2]])
# LISTA_PUNTOS = np.array(LISTA_PUNTOS)
# np.shape(LISTA_PUNTOS)

# La lista de puntos ahora son las intersecciones del grid
LISTA_PUNTOS = grid.puntos_interseccion(RGB2, 10)
print("Numero de puntos: {}".format(len(LISTA_PUNTOS)))
import mean_shift_epanechnikov as ms
#Utilizar el algoritmo meanshift sobre la lista de puntos. 5 Dimensiones + 1 de la clasificación
mean_shifter = ms.MeanShift(kernel = 'epanechnikov_kernel')
#ORIGINALMENTE ERA [0.2,0.2]
mean_shift_result = mean_shifter.cluster(LISTA_PUNTOS, kernel_bandwidth = [100,255])

# Muestra las asignaciones de cada uno de los puntos
cluster_assignments = mean_shift_result.cluster_ids
print(cluster_assignments)
#print(bayesian.get_small_clusters(cluster_assignments,1))
new_assignments = bayesian.reduce_clusters(mean_shift_result,10)
print(new_assignments)
mean_shift_result.cluster_ids=new_assignments
res = grid.visualizar_clusteres(RGB2,mean_shift_result)

img = Image.fromarray(res,'RGB')
img.save('cluster_sea.png','png')

bayesian = bayesian.BayesianClassifier(mean_shift_result)
bayesian.show_classifiers()

LISTA_PUNTOS_BAYESIAN=grid.puntos_interseccion(RGB2, 1) #toda la imagen
bayesian_clustering = bayesian.cluster_data_points(LISTA_PUNTOS_BAYESIAN)
print(bayesian_clustering)

bayesian_result = ms.MeanShiftResult(LISTA_PUNTOS_BAYESIAN,np.zeros(1),bayesian_clustering)
res_b = grid.visualizar_clusteres(RGB2,bayesian_result)

img = Image.fromarray(res_b,'RGB')
img.save('bayesian.png','png')

x_y_c = foreground_estimation.cambia_formato(mean_shift_result)
f_estimator =   foreground_estimation.foreground_estimation(x_y_c)
fe_scores = f_estimator.predictor()
print(fe_scores)
