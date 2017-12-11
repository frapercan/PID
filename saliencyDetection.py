from skimage import io, color, filters
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

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






def generar_grid(tam,tam_celda):
    res = []
    fila = 
    for i in range(tam):
        if(i % tam_celda == 0):
            fila 
            
        
    
