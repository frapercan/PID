# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:30:01 2017
Procesamiento de Imagenes Digitales.



28/12: metidas todas las funciones antiguas que hizo Ángel




"""

import numpy as np
import random
from skimage import io, color,filters
import itertools as it


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


def visualizar_clusteres(imagen_original,mean_shift_result,formato="RGB"):
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
    resultado = imagen_original #np.zeros((shape),dtype='uint8')
    resultado.flags.writeable = True

    if(formato=="LAB"):
        puntos_originales = list(mean_shift_result.original_points)
    elif(formato=="HSV"):
        puntos_originales = color.lab2rgb(list(mean_shift_result.original_points))
    else:
        puntos_originales = list(mean_shift_result.original_points)

    #Le metí que genere un color aleatorio por cada cluster para poder ver con claridad los clusteres y que
    # no se confundan con la imagen
    random_color = lambda: random.randint(0,255)

    for (i,j) in list(enumerate(mean_shift_result.cluster_ids)):
        if not (j in clases):
            clases.update({j:[random_color(),random_color(),random_color()]})
        color = clases.get(j)
        resultado[int(puntos_originales[i][0]),int(puntos_originales[i][1])]= color
    return resultado

def generar_imagen_con_grid(array_imagen,tam_celda):
    shape = np.shape(array_imagen)
    def suma_pixel(l1,l2):
        r1 = 255 if l2[0] == 255 else l1[0]
        r2 = 255 if l2[1] == 255 else l1[1]
        r3 = 255 if l2[2] == 255 else l1[2]
        return [r1,r2,r3]
    def suma_imagenes(arr1,arr2):
        return [[suma_pixel(arr1[y][x],arr2[y][x]) for x in range(shape[1])] for y in range(shape[0])]

    grid = generar_grid_a_traves_imagen_y_opcion(array_imagen,tam_celda,1)
    resultado = suma_imagenes(array_imagen,grid)
    return np.array(resultado,dtype='uint8')

def generar_grid_a_traves_imagen_y_opcion(array_imagen,tam_celda,opcion=0):
    shape = np.shape(array_imagen)
    if(opcion == 0):
        return generar_puntos_interseccion_grid(shape[1],shape[0],tam_celda)
    else:
        return generar_grid_entero(shape[1],shape[0],tam_celda)

def generar_grid_entero(tam_x,tam_y,tam_celda):
    #Inicialización grid
    grid = []
    #Tipo1: Tipo de fila que va alternando entre blanco y negro.
    #Tipo2: Tipo de fila que es toda blanca.
    #Iterador del tipo de Fila 1
    def tipo1():
        #n: valor que va incrementandose hasta alcanzar el tamaño en x de la imagen
        #m: valor que se va actualizando que informa si se ha traspasado el tamaño de una celda (en x) en cada iteración
        n = 0
        m = 0
        while n < tam_x:
            if(m == 0):
                yield [255,255,255]
                m = tam_celda
            else:
                yield [0,0,0]
                m -=1
            n+=1
    #Creación de los arrays genericos del tipo1 y tipo2 a traves de dos listas y pasandoles iteradores
    tipo1 = np.array(list(tipo1()),dtype='uint8')
    tipo2 = np.array(list(it.repeat([255,255,255],tam_x)),dtype='uint8')
    #Inicialización de un valor para controlar la separación entre celdas.
    m = 0
    #Unión de las filas teniendo en cuenta la separación entre celdas.
    for _ in range(tam_y):
        if(m == 0):
            grid.append(tipo2)
            m = tam_celda
        else:
            grid.append(tipo1)
            m-=1
    return np.array(grid,dtype='uint8')


def puntos_interseccion(array_imagen,tam_celda):
    grid = generar_grid_a_traves_imagen_y_opcion(array_imagen,tam_celda)
    resultado = []
    for (y,x) in grid:
        resultado.append([y,x]+list(array_imagen[y][x]))
    return np.array(resultado)

def generar_puntos_interseccion_grid(tam_x,tam_y,tam_celda):

    #dato -> (pos_x,pos_y)
    def iterador_grid():
        #a: valor que va incrementandose hasta alcanzar el tamaño en x de la imagen
        #b: valor que va incrementandose hasta alcanzar el tamaño en y de la imagen
        #m: valor que se va actualizando que informa si se ha traspasado el tamaño de una celda (en x) en cada iteración
        a = 0
        b = 0
        m = 1
        while b < tam_y:
            while a < tam_x:
                if(m == 0):
                    yield (b,a)
                    m = tam_celda
                else:
                    m-=1
                a+=1
            b+=tam_celda+1
            m=1
            a=0
    return list(iterador_grid())
