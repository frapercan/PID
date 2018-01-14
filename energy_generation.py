# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 03:28:10 2017

"""
import pylab
import PIL
from PIL import Image, ImageFilter
import grid_utils
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io, color,filters
plt.interactive(True)
class energy_generation(object):
    """
    Clase que coge un foreground estimation en donde se diferencia fondo y figura (tras k-means con k=2)
    
    Formato de entrada: 
        x_y_c: Lista con esta sintaxis [(x,y,0||1)...(x,y,0||1)] (cero para fondo, uno para figura)
        shape: Tamaño de la imagen
        tam_celda: Tamaño de la celda del mismo grid usado para el meanshift.
    """
    
    def __init__(self,x_y_c,shape,tam_celda,nombre):
        self.x_y_c = x_y_c
        self.shape = shape
        self.tam_celda = tam_celda
        self.nombre = nombre
    
    def hacer_saliency_map(self):
        
        self.interseccion_grid_figura()
        img = Image.fromarray(self.res,'L')
        img.save('morfologia.png','png')
        self.morfologia()
        img = Image.fromarray(self.res,'L')
        #img = PIL.ImageOps.invert(img)
        img.save('morfologia1.png','png')
        
        self.res = np.array(io.imread("morfologia1.png"))
        """
        Euclidean distance transform, sacado de http://www.logarithmic.net/pfh/blog/01185880752
        """
        
        
#        def escaneado(f):
#            for i, fi in enumerate(f):
#                if (fi != np.inf):
#                    for j in range(1,i+1):
#                        x = fi+j*j
#                        if f[i-j] >= x:
#                            f[i-j] = x
#        
#        def transformacion_distancia(array_binario):
#            f = np.where(array_binario, np.inf, 0.0)
#            print(f)
#            pylab.imshow(f)
#            pylab.show()
#            pylab.clf()
#            for i in range(f.shape[0]):
#                escaneado(f[i,:])
#                escaneado(f[i,::-1])
#            for i in range(f.shape[1]):
#                escaneado(f[:,i])
#                escaneado(f[::-1,i])
#            np.sqrt(f,f)
#            return f
#        print("a")
        data = ndimage.distance_transform_edt(self.res)
#        print(data)
#        print("b")

        cmap = plt.cm.jet
        norm = plt.Normalize(vmin=data.min(), vmax=data.max())
        image = cmap(norm(data))
        plt.imsave(self.nombre, image)
#        imshow()
#        pylab.show()
#        pylab.savefig()
        return data
        
        
    
    def interseccion_grid_figura(self):
        """
        Formar un grid con los puntos aislados clasificados como figura.
        """
        
        """
        Idea: Primero se hace una cruz de color blanco en los puntos que son figura. Despues se evaluan los fondos, haciendo cruces
        de color negro.
        
        """
        
        #invertir a 0 para invertir
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
        for (x,y) in lista_fondos:
            for i in range(self.tam_celda):
                    if(x+(i+1) < self.shape[0]):
                        res[x+(i+1),y] = 255
                    if(y+(i+1) < self.shape[1]):    
                        res[x,y+(i+1)] = 255
                    if(x-(i+1) >= 0):
                        res[x-(i+1),y] = 255
                    if(y-(i+1) >= 0):
                        res[x,y-(i+1)] = 255
        self.res = res
        
    def morfologia(self):
        
        """
        Se exploran todos los puntos blancos en cada fila.
        Si no hay puntos blancos en esa fila, se pasa a la siguiente.
        En caso contrario, se van almacenando en una lista.
        Una vez hecho eso, se prepara para que pueda accederse como pares de un elemento y su siguiente.
        Se accede al primer elemento, para poner pixeles blancos a la izquierda si procede (su distancia
        a la izquiera es menor que el tamaño de la celda)
        Una vez hecho eso, se añade por la derecha pixeles blancos comprobando las distancias de los
        pixeles de la lista de un elemento con el siguiente.
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
        
    
    
    
