# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 03:28:10 2017

"""



from PIL import Image
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io
plt.interactive(True)


"""
Funcion de utilidad que unifica los tres mapas de profundidad, haciendo la media pixel a pixel.
Guarda en un fichero una unificación de los tres mapas y además devuelve como salida los datos
de la media de los 3 mapas de profundidad.

"""
def unificar_eg(prof1,prof2,prof3,directorio_salida):
    prof_media = list()
    for i,p1 in enumerate(prof1):
        subl = list()
        for pix1,pix2,pix3 in zip(p1,prof2[i],prof3[i]):
            subl.append((pix1+pix2+pix3)/3)
        prof_media.append(subl)
    data = np.array(prof_media)
    cmap = plt.cm.jet_r
    norm = plt.Normalize(vmin=data.min(), vmax=data.max())
    image = cmap(norm(data))
    plt.imsave(directorio_salida+"profundidad_unificado.jpg", image)
    return data
    
class energy_generation(object):
    """
    Clase que coge un foreground estimation en donde se diferencia fondo y figura (tras k-means con k=2)
    
    Formato de entrada: 
        x_y_c: Lista con esta sintaxis [(x,y,0||1)...(x,y,0||1)] (cero para fondo, uno para figura)
        shape: Tamaño de la imagen
        tam_celda: Tamaño de la celda del mismo grid usado para el meanshift.
        nombre_salida: Nombre del fichero en donde se guardara la imagen de salida con el resultado del energy generation
        nombre_grid_interseccion_figura: Nombre del fichero en donde se guardara la imagen de salida con el resultado del grid formado por los puntos aislados
        nombre_morfologia: Nombre del fichero en donde se guardara la imagen de salida con el resultado de la morfologia aplicada al grid formado por los puntos aislados
    """
    
    """
    Constructor de la clase
    """
    
    def __init__(self,x_y_c,shape,tam_celda,nombre_salida,nombre_grid_interseccion_figura,nombre_morfologia):
        self.x_y_c = x_y_c
        self.shape = shape
        self.tam_celda = tam_celda
        self.nombre_salida = nombre_salida
        self.nombre_grid_interseccion_figura = nombre_grid_interseccion_figura
        self.nombre_morfologia = nombre_morfologia
    
        
    """
    Funcion que se dedica a hacer los calculos de toda la clase.
    Esta función crea todas las imagenes intermedias para asi poder hacer finalmente el saliency map, además de este.
    Para este ultimo, se hace una transformación de distancia del resultado de la morfologia y se 
    guarda como
    """
    def hacer_saliency_map(self):
        
        self.interseccion_grid_figura()
        img = Image.fromarray(self.res,'L')
        img.save(self.nombre_grid_interseccion_figura,'png')
        self.morfologia()
        img = Image.fromarray(self.res,'L')
        img.save(self.nombre_morfologia,'png')
        self.res = np.array(io.imread(self.nombre_morfologia))
        data = ndimage.distance_transform_edt(self.res)
        cmap = plt.cm.jet_r
        norm = plt.Normalize(vmin=data.min(), vmax=data.max())
        image = cmap(norm(data))
        plt.imsave(self.nombre_salida, image)
        return data
    """
    Esta función forma la intersección de los puntos aislados en forma de grid, de forma que dos puntos aislados
    se unen si estan a una distancia igual al tamaño de celda y además, esos puntos han sido clasificados como figura.
    """        
        
    
    def interseccion_grid_figura(self):
        
        res = np.asarray(list(it.repeat(list(it.repeat(255,self.shape[1])),self.shape[0])),dtype='uint8')
        lista_fondos = []
        for (x,y,c) in self.x_y_c:
            if (c == 1):
                res[x,y] = 0
                for i in range(self.tam_celda):
                    if(x+(i+1) < self.shape[0]):
                        res[x+(i+1),y] = 0
                    if(y+(i+1) < self.shape[1]):    
                        res[x,y+(i+1)] = 0
                    if(x-(i+1) >= 0):
                        res[x-(i+1),y] = 0
                    if(y-(i+1) >= 0):
                        res[x,y-(i+1)] = 0
            else:
                lista_fondos.append((x,y))
        self.res = res
        
    def morfologia(self):
        
        """
        Se hace una morfologia en la que se rellenan los grids formados anteriormente que formen cuadrados con el tamaño de la celda.
        """
        res = self.res
        for x in range(self.shape[0]):
            lista_puntos = []
            for y in range(self.shape[1]):
                if(res[x,y] == 0):
                    lista_puntos.append(y)
            if(lista_puntos != []):
                lista_elem_y_sig = list(zip(lista_puntos,lista_puntos[1:]+lista_puntos[:1]))[:-1]
                lista_elem_y_sig.append((lista_puntos[-1],self.shape[1]-1))
                if(lista_elem_y_sig[0][0] <= self.tam_celda+1):
                    for t in range(self.tam_celda):
                                if(lista_puntos[0]-(t+1) >=0):
                                    res[x,lista_puntos[0]-(t+1)] = 0
                for act,sig in lista_elem_y_sig:   
                    if(sig-act <= self.tam_celda+1):
                            for t in range(sig-act):
                                if(act+t+1 < self.shape[1]):
                                    res[x,act+t+1] = 0
        self.res = res
        
    
    
    
