from PIL import Image, ImageOps
from .models import Imagen, Prueba
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
import itertools as it
import mean_shift as ms

def call_to_action(image_pk,test_pk):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    image_for_pil = Image.fromarray(generar_imagen_con_grid(np.array(image_for_pil),30))
    image_for_pil.save("temp/edited_.png","png")

    fil = open("temp/edited_.png", 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre=image_selected.nombre,archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test = Prueba.objects.get(pk=test_pk)
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url


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
