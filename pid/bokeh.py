# -*- coding: utf-8 -*-
import numpy as np
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import PIL
import matplotlib.pyplot as plt

class bokeh(object):

    def __init__(self,nombre_imagen_original,nombre_thumbnail,nombre_superpixel):
        self.nombre_imagen_original = nombre_imagen_original
        self.nombre_thumbnail = nombre_thumbnail
        self.nombre_superpixel = nombre_superpixel

    def difuminacion_gaussiana_fondo(self):
        imagen_original = PIL.Image.open(self.nombre_imagen_original)
        imagen_superpixel = PIL.Image.open(self.nombre_superpixel).convert('L')

        a = np.shape(imagen_original)
        imagen_superpixel=  imagen_superpixel.resize((a[1],a[0]), PIL.Image.ANTIALIAS)
        imagen_superpixel=  imagen_superpixel.filter(PIL.ImageFilter.GaussianBlur(1.3))
        imagen_superpixel.save("superpixelgrande.png")

        imagen_original  = PIL.Image.open(self.nombre_imagen_original).convert("RGBA")
        imagen_original2 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(3))
        imagen_original3 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(7))
        imagen_original4 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(9))
        imagen_original5 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(10))

        imagen_superpixel = PIL.Image.open("superpixelgrande.png").convert('L')
        array_superpixel = np.array(imagen_superpixel)
        array_superpixel.setflags(write=True)
        array_superpixel_thumbnail_nivel_fondo  = np.where(array_superpixel > -1, 255, 0)
        array_superpixel_thumbnail_nivel_medio3  = np.where(array_superpixel > 50, 255, 0)
        array_superpixel_thumbnail_nivel_medio2  = np.where(array_superpixel > 100, 255, 0)
        array_superpixel_thumbnail_nivel_medio1  = np.where(array_superpixel > 150, 255, 0)
        array_superpixel_thumbnail_nivel_figura = np.where(array_superpixel > 200, 255, 0)

        io.imsave("aaa.png",array_superpixel_thumbnail_nivel_fondo)
        io.imsave("bbb.png",array_superpixel_thumbnail_nivel_medio1)
        io.imsave("bbb2.png",array_superpixel_thumbnail_nivel_medio2)
        io.imsave("bbb3.png",array_superpixel_thumbnail_nivel_medio3)
        io.imsave("ccc.png",array_superpixel_thumbnail_nivel_figura)

        imagen_superpixel_fondo = PIL.Image.open("aaa.png").convert('L')
        imagen_superpixel_medio1 = PIL.Image.open("bbb.png").convert('L')
        imagen_superpixel_medio2 = PIL.Image.open("bbb2.png").convert('L')
        imagen_superpixel_medio3 = PIL.Image.open("bbb3.png").convert('L')
        imagen_superpixel_figura = PIL.Image.open("ccc.png").convert('L')

        final1 = PIL.Image.new("RGBA", imagen_original.size)
        final1.paste(imagen_original5, (0,0), imagen_superpixel_fondo)
        final1.paste(imagen_original4, (0,0), imagen_superpixel_medio3)
        final1.paste(imagen_original3, (0,0), imagen_superpixel_medio2)
        final1.paste(imagen_original2, (0,0), imagen_superpixel_medio1)
        final1.paste(imagen_original, (0,0), imagen_superpixel_figura)
        final1 = final1.filter(PIL.ImageFilter.SMOOTH)
        final1.save("gauss_adaptativo.png")
