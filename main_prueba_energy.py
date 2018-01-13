# -*- coding: utf-8 -*-
if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""

"""
Clase de prueba Energy Generation
"""


import PIL
import skimage
from skimage import transform
from PIL import Image, ImageFilter
from skimage import io, color,filters
import numpy as np
import random
import energy_generation
from PIL import ImageOps


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
    
import itertools
import foreground_estimation
from scipy.cluster.vq import kmeans,vq,whiten
import grid_utils as grid
#Extraer los puntos de la imagen que tienen intersección con el Grid
#ORIGINALMENTE ERAN 100


#thumbnail = grid.thumbnail("balloon.jpg",(200,200))

RGB = np.array(io.imread("balloon.jpg"))



LISTA_PUNTOS = grid.puntos_interseccion(RGB, 5)
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
fe_estimator = foreground_estimation.foreground_estimation(x_y_c)
#puntos_clasificados = fe_estimator.classify_points()

#fe_scores = fe_estimator.predictor()
#print(fe_scores)
#normalizacion= whiten(fe_scores)
#normalizacion = normalizacion.reshape(-1,1)
#print(normalizacion)
#centroides,_ = kmeans(normalizacion,k_or_guess=2)
#clases,_ = vq(fe_scores.reshape(-1,1),centroides)
#
#print(centroides)
#print(clases)
#
#lista = [[x,y,clases[c]] for x,y,c in x_y_c]
#print(np.shape(lista))
#print(np.shape(fe_estimator.classify_points()))

puntos_clasificados = fe_estimator.classify_points()
#print(fe_scores[clases==0])
#print(fe_scores[clases==1])
#from sklearn.cluster import KMeans
#import numpy as np
#x = np.random.random(np.shape(fe_scores)[0])


#km = KMeans(n_clusters=2)
#print(normalizacion.reshape(-1,1))
#km.fit(normalizacion.reshape(-1,1))
#km.predict()


#cambia_clase_n_primeros(x_y_c,20)
#cambia_clase(x_y_c)
#print(x_y_c)
eg = energy_generation.energy_generation(puntos_clasificados,np.shape(RGB),10)
eg.hacer_saliency_map()



