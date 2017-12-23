# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.
"""

from PIL import Image
from skimage import io, color
import numpy as np

##Imagen de muestra en el mismo directorio del archivo
RGB = np.array(io.imread("sea.jpg"))

LAB = np.array(color.rgb2lab(RGB))

HSV = np.array(color.rgb2hsv(RGB))

##Aplicamos los filtros gaussianos y almacenamos en variables
#GAUSSIAN_KERNELS = [1, 3, 5]

#RGB1 = filters.gaussian(RGB,GAUSSIAN_KERNELS[0])
#RGB2 = filters.gaussian(RGB,GAUSSIAN_KERNELS[1])
#RGB3 = filters.gaussian(RGB,GAUSSIAN_KERNELS[2])
#
#LAB1 = filters.gaussian(LAB,GAUSSIAN_KERNELS[0])
#LAB2 = filters.gaussian(LAB,GAUSSIAN_KERNELS[1])
#LAB3 = filters.gaussian(LAB,GAUSSIAN_KERNELS[2])
#
#HSV1 = filters.gaussian(HSV,GAUSSIAN_KERNELS[0])
#HSV2 = filters.gaussian(HSV,GAUSSIAN_KERNELS[1])
#HSV3 = filters.gaussian(HSV,GAUSSIAN_KERNELS[2])

import grid_utils as grid
#Extraer los puntos de la imagen que tienen intersección con el Grid
#ORIGINALMENTE ERAN 100



LISTA_PUNTOS = grid.extrae_puntos_grid_imagen(RGB, 600)
print(np.shape(LISTA_PUNTOS))
import mean_shift_epanechnikov as ms
#Utilizar el algoritmo meanshift sobre la lista de puntos. 5 Dimensiones + 1 de la clasificación

mean_shifter = ms.MeanShift(kernel = 'epanechnikov_kernel')
#ORIGINALMENTE ERA [0.2,0.2]
mean_shift_result = mean_shifter.cluster(LISTA_PUNTOS, kernel_bandwidth = [30,30])

#img = Image.fromarray(mean_shift_result.shifted_points,'RGB')
#img.save('a.png')