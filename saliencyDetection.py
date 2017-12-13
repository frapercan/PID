from skimage import io, color, filters
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import itertools as it
from matplotlib import pyplot as plt
from PIL import Image

rgb = io.imread("sea.jpg")

lab = color.rgb2lab(rgb)

hsv = color.rgb2hsv(rgb)


gaussian_kernels = [1,3,5]

rgb1 = filters.gaussian(rgb,gaussian_kernels[0])
rgb2 = filters.gaussian(rgb,gaussian_kernels[1])
rgb3 = filters.gaussian(rgb,gaussian_kernels[2])

lab1 = filters.gaussian(lab,gaussian_kernels[0])
lab2 = filters.gaussian(lab,gaussian_kernels[1])
lab3 = filters.gaussian(lab,gaussian_kernels[2])

hsv1 = filters.gaussian(hsv,gaussian_kernels[0])
hsv2 = filters.gaussian(hsv,gaussian_kernels[1])
hsv3 = filters.gaussian(hsv,gaussian_kernels[2])
#No sabemos si los filtros gaussianos se aplican bien, se muestran verde al pasar de lab y hsv a rgb y mostrarlo
lista_saliency_map = [rgb1,rgb2,rgb3,lab1,lab2,lab3]

# Genera una lista solo con los puntos de intersección del grid
def generar_puntos_interseccion_grid(tam_x,tam_y,tam_celda):
    
    #dato -> (pos_x,pos_y)
    def iterador_grid():
        #a: valor que va incrementandose hasta alcanzar el tamaño en x de la imagen
        #b: valor que va incrementandose hasta alcanzar el tamaño en y de la imagen
        #m: valor que se va actualizando que informa si se ha traspasado el tamaño de una celda (en x) en cada iteración
        a = 0
        b = 0
        m = 0
        while b < tam_y:
            while a < tam_x:
                if(m == 0):
                    yield (b,a)
                    m = tam_celda
                else:
                    m-=1
                a+=1
            b+=tam_celda+1
            m=0
            a=0
    return list(iterador_grid())

# Genera el array de la imagen del grid.       
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



#Genera un grid segun una imagen como array de numpy. Tiene dos opciones, o bien solo los pixeles de la intersección del grid (I) o bien todo el grid (otro)
def generar_grid_a_traves_imagen_y_opcion(array_imagen,tam_celda,opcion=0):
    shape = np.shape(array_imagen)
    if(opcion == 0):
        return generar_puntos_interseccion_grid(shape[1],shape[0],tam_celda)
    else:
        return generar_grid_entero(shape[1],shape[0],tam_celda)

#Genera la misma imagen pasada por parametros con un grid solapado.
def generar_imagen_con_grid(nombre_fichero,array_imagen,tam_celda):
   pass #TODO
    
    


#Genera una imagen solo con los puntos de intersección del grid con la imagen pasada por parametros.
def generar_imagen_interseccion(nombre_fichero,array_imagen,tam_celda):
    
    def puntos_interseccion(array_imagen,tam_celda):
        grid = generar_grid_a_traves_imagen_y_opcion(array_imagen,tam_celda)
        resultado = []
        for (y,x) in grid:
            resultado.append((y,x,array_imagen[y][x]))
        return resultado
    
    shape = np.shape(array_imagen)
    interseccion = puntos_interseccion(array_imagen,tam_celda)
    resultado = [[[127,127,127] for x in range(shape[1])] for y in range(shape[0])]
    for (y,x,dato) in interseccion:
        resultado[y][x] = dato
    io.imsave(nombre_fichero,np.array(resultado,dtype='uint8'))
    
#Comandos de prueba
#generar_imagen_interseccion('imagen_interseccion.png',rgb,1)
#generar_imagen_interseccion('imagen_interseccion2.png',rgb,10)

#io.imsave('celda.png',generar_grid_a_traves_imagen_y_opcion(rgb,10,1))
