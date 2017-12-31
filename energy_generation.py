# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 03:28:10 2017

"""

import grid_utils

class energy_generation(object):
    """
    Clase que coge un foreground estimation en donde se diferencia fondo y figura (tras k-means con k=2)
    
    Formato de entrada: 
        x_y_c: Lista con esta sintaxis [(x,y,"fondo"||"figura")...(x,y,"fondo"||"figura")]
        shape: Tamaño de la imagen
        tam_celda: Tamaño de la celda del mismo grid usado para el meanshift.
    """
    
    def __init__(self,x_y_c,shape,tam_celda):
        self.x_y_c = x_y_c
        self.shape = shape
        self.tam_celda = tam_celda
    
    def hacer_saliency_map(self):
        
        self.interseccion_grid_figura()
        self.morfologia()
        """
        
        Aplicar una transformacion de distancia a la imagen con morfologia.
        
        
        (operaciones...)
        
        
        
        
        return 
        """
        
    
    def interseccion_grid_figura(self):
        """
        Primero se hace un grid entero (lineas blancas y fondo negro).
        
        Si la figura al final se decide que es un area, se hace una interseccion normal y corriente.
        
        Si la figura al final se decide que son puntos aislados, se hace la interseccion normal y 
        corriente con esos puntos aislados y despues se quitan las lineas blancas
        que no tengan dos extremos.
        
        Es decir, se quitan lineas del estilo:
            x----
            
            ó
            
            |
            |
            |
            |
            x
            
            y viceversa
            
        Pero no se quitan:
            
            x----x
            
            ó
            
            x
            |
            |
            |
            |
            x
            
        Siendo x, la interseccion del grid.
        
        """
        array_imagen = np.zeros(self.shape)
        grid = generar_grid_a_traves_imagen_y_opcion(array_imagen,self.tam_celda,opcion=1)
        
        """
        operaciones (...)
        
        self.res = res
        """
        pass
        
    def morfologia(self):
        
        """
        
        Se coge el self.interseccion y se va evaluando fila por fila del array.
        
        Se va buscando el primer punto blanco en cada fila.
        Si no encuentra punto blanco en una fila, no se hace nada
        
        Si se encuentra el primer punto blanco de esa fila, se almacena su posicion, y se busca el siguiente.
            Si no hay mas puntos blancos, no se hace nada.
            Si hay otro punto blanco, se almacena su posicion.
                Si tras este hay otro punto blanco, se sobrescribe su posicion.
        Tras finalizar la fila, se sustituye los extremos de las dos posiciones por puntos blancos.
        
        
        operaciones (...)
        
        
        self.res = res
        
        """
        
        pass
    
    
    
