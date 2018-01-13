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
np.set_printoptions(threshold=np.inf)

image = img_as_float(io.imread("jakob-nielsen-thumbs-up.jpg"))
profundidad = img_as_float(io.imread("transformacion_distancia.jpg"))

segmentos = slic(image, n_segments = 8, sigma = 10)
print(segmentos)
segmentos = np.ndarray.flatten(segmentos)

print(segmentos)

#for s,p in zip(segmentos,profundidad):
#    print(p)
#    diccionario = {}
#    if(not(s in diccionario)):
#        s = p
#    else:
#        if(p > diccionario[s]):
#            diccionario[s]=p
#data = diccionario
#
#cmap = plt.cm.Greys
#norm = plt.Normalize(vmin=data.min(), vmax=data.max())
#image = cmap(norm(data))
#plt.imsave("superpixel.jpg", image)
#fig = plt.figure("aaaaa")
#ax = fig.add_subplot(1, 1, 1)
#ax.imshow(mark_boundaries(image, segmentos))
#print(segmentos)
#plt.show()
