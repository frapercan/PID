# -*- coding: utf-8 -*-
import numpy as np
from skimage import io
import PIL

"""
Clase que implementa el bokeh de forma parcial (no hace el efecto de difuminar las luces con las lentes)

"""



class bokeh(object):
    
    """
    Constructor:
        nombre_imagen_original: Nombre de la imagen original.
        nombre_thumbnail: Nombre de la imagen thumbnail.
        nombre_superpixel: Nombre de la imagen de superpixel.
        directorio_metadatos: Ruta del directorio de metadatos.
        directorio_resultados: Ruta del directorio del directorio de resultados.
    
    """
    
    def __init__(self,nombre_imagen_original,nombre_thumbnail,nombre_superpixel,directorio_metadatos,directorio_resultados):
        self.nombre_imagen_original = nombre_imagen_original
        self.nombre_thumbnail = nombre_thumbnail
        self.nombre_superpixel = nombre_superpixel
        self.directorio_metadatos = directorio_metadatos
        self.directorio_resultados = directorio_resultados
        self.nombre_fichero_salida = nombre_imagen_original[:-4]+ " "
        
    """
    Esta función hace un difuminado poco a poco segun los niveles de grises de la imagen formada
    por el superpixel con el mapa de profundidad. A mas gris en la imagen del superpixel con el mapa de profundidad, 
    más difuminación en la imagen original.
    
    Devuelve la imagen original en un fichero con el difuminado.
    
    """
    
    
    def difuminacion_gaussiana_fondo(self):
        imagen_original = PIL.Image.open(self.nombre_imagen_original)
        imagen_superpixel = PIL.Image.open(self.nombre_superpixel).convert('L')
        
        a = np.shape(imagen_original)
        imagen_superpixel=  imagen_superpixel.resize((a[1],a[0]), PIL.Image.ANTIALIAS)
        imagen_superpixel=  imagen_superpixel.filter(PIL.ImageFilter.GaussianBlur(1.3))
        imagen_superpixel.save(self.directorio_metadatos+"superpixelgrande.png")
        
        imagen_original  = PIL.Image.open(self.nombre_imagen_original).convert("RGBA")
        imagen_original2 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(3))
        imagen_original3 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(7))
        imagen_original4 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(9))
        imagen_original5 = imagen_original.filter(PIL.ImageFilter.GaussianBlur(10))

        imagen_superpixel = PIL.Image.open(self.directorio_metadatos+"superpixelgrande.png").convert('L')
        array_superpixel = np.array(imagen_superpixel)
        array_superpixel.setflags(write=True)
        array_superpixel_thumbnail_nivel_fondo   = np.where(array_superpixel > -1, 255, 0)
        array_superpixel_thumbnail_nivel_medio3  = np.where(array_superpixel > 50, 255, 0)
        array_superpixel_thumbnail_nivel_medio2  = np.where(array_superpixel > 100, 255, 0)
        array_superpixel_thumbnail_nivel_medio1  = np.where(array_superpixel > 150, 255, 0)
        array_superpixel_thumbnail_nivel_figura  = np.where(array_superpixel > 200, 255, 0)

        io.imsave(self.directorio_metadatos+"Nivel_fondo.png",array_superpixel_thumbnail_nivel_fondo)
        io.imsave(self.directorio_metadatos+"Nivel_medio_posterior.png",array_superpixel_thumbnail_nivel_medio1)
        io.imsave(self.directorio_metadatos+"Nivel_medio_medio.png",array_superpixel_thumbnail_nivel_medio2)
        io.imsave(self.directorio_metadatos+"Nivel_medio_anterior.png",array_superpixel_thumbnail_nivel_medio3)
        io.imsave(self.directorio_metadatos+"Nivel_figura.png",array_superpixel_thumbnail_nivel_figura)

        imagen_superpixel_fondo  = PIL.Image.open(self.directorio_metadatos+"Nivel_fondo.png").convert('L')
        imagen_superpixel_medio1 = PIL.Image.open(self.directorio_metadatos+"Nivel_medio_anterior.png").convert('L')
        imagen_superpixel_medio2 = PIL.Image.open(self.directorio_metadatos+"Nivel_medio_medio.png").convert('L')
        imagen_superpixel_medio3 = PIL.Image.open(self.directorio_metadatos+"Nivel_medio_posterior.png").convert('L')
        imagen_superpixel_figura = PIL.Image.open(self.directorio_metadatos+"Nivel_figura.png").convert('L')

        aux1 = PIL.Image.new("RGBA", imagen_original.size)
        aux1.paste(imagen_original5, (0,0), imagen_superpixel_fondo)
        aux1.save(self.directorio_metadatos+"partes_gaussiano_1"+".png")
        
        
        aux2 = PIL.Image.new("RGBA", imagen_original.size)
        aux2.paste(imagen_original4, (0,0), imagen_superpixel_medio1)
        aux2.save(self.directorio_metadatos+"partes_gaussiano_2"+".png")
        
        aux3 = PIL.Image.new("RGBA", imagen_original.size)
        aux3.paste(imagen_original3, (0,0), imagen_superpixel_medio2)
        aux3.save(self.directorio_metadatos+"partes_gaussiano_3"+".png")
        
        
        aux4 = PIL.Image.new("RGBA", imagen_original.size)
        aux4.paste(imagen_original2, (0,0), imagen_superpixel_medio3)
        aux4.save(self.directorio_metadatos+"partes_gaussiano_4"+".png")
        
        aux5 = PIL.Image.new("RGBA", imagen_original.size)
        aux5.paste(imagen_original, (0,0), imagen_superpixel_figura)
        aux5.save(self.directorio_metadatos+"partes_gaussiano_5"+".png")
        
        
        final = PIL.Image.new("RGBA", imagen_original.size)
        final.paste(imagen_original5, (0,0), imagen_superpixel_fondo)     
        final.paste(imagen_original4, (0,0), imagen_superpixel_medio3)
        
        final.paste(imagen_original3, (0,0), imagen_superpixel_medio2)
        
        final.paste(imagen_original2, (0,0), imagen_superpixel_medio1)
        
        final.paste(imagen_original, (0,0), imagen_superpixel_figura)
        final = final.filter(PIL.ImageFilter.SMOOTH)
        final.save(self.directorio_resultados+self.nombre_fichero_salida+"_gaussiano_segun_superpixel"+".png")
          

