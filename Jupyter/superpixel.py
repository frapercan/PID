# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:18:33 2018

PID
"""
import numpy as np
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt

"""
Clase que implementa las funcionalidades de trabajo con superpixel.
"""


class superpixel(object):
    """
    Constructor:
        nombre_thumbnail: Nombre del thumbnail de la imagen original
        profundidad: Mapa de profundidad en formato array.
        nombre_salida: Nombre de la imagen de salida.
    """
    
    def __init__(self,nombre_thumbnail,profundidad,nombre_salida):
        self.nombre_thumbnail = nombre_thumbnail
        self.profundidad = profundidad
        self.nombre_salida = nombre_salida
    
    """
    Esta función hace el superpixel del thumbnail. Tras eso, accede a las regiones del superpixel y va mirando los
    valores mas alto de cada región del superpixel en el mapa de profundidad y le asigna el mas alto. Con eso se consigue
    un mapa superpixel de profundidad.
    """
        
    def hacer_superpixel(self):
        image = img_as_float(io.imread(self.nombre_thumbnail))
        segmentos = slic(image, n_segments = 200, sigma = 5)
        segmentos2 = np.ndarray.flatten(segmentos)
        profundidad = np.ndarray.flatten(self.profundidad)
        diccionario = {}
        for s,p in zip(segmentos2,profundidad): 
            if(not(s in diccionario)):
                diccionario[s] = p
            else:
                if(p > diccionario[s]):
                    diccionario[s]=p
        data = diccionario

        superpixel = list()

        for s in segmentos:
            subl = list()
            for s1 in s:
                subl.append(diccionario[s1])
            superpixel.append(subl)
        data = np.asarray(superpixel)
        cmap = plt.cm.Greys
        norm = plt.Normalize(vmin=data.min(), vmax=data.max())
        image = cmap(norm(data))
        plt.imsave(self.nombre_salida, image)