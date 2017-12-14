from skimage import io, color
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab



RGB = np.array(io.imread("sea.jpg"))

LAB = np.array(color.rgb2lab(RGB))

HSV = np.array(color.rgb2hsv(RGB))


#GAUSSIAN_KERNELS = [1, 3, 5]

#RGB1 = filters.gaussian(RGB,GAUSSIAN_KERNELS[0])
#RGB2 = filters.gaussian(RGB,GAUSSIAN_KERNELS[1])
#RGB3 = filters.gaussian(RGB,GAUSSIAN_KERNELS[2])
#
#LAB1 = filters.gaussian(LAB,GAUSSIAN_KERNELS[0])
#LAB2 = filters.gaussian(LAB,GAUSSIAN_KERNELS[1])
#LAB3 = filters.gaussian(LAB,GAUSSIAN_KERNELS[2])
#
#HSV1 = filters.gaussian(HSV,GAUSSIAN_KERNELS[0])
#HSV2 = filters.gaussian(HSV,GAUSSIAN_KERNELS[1])
#HSV3 = filters.gaussian(HSV,GAUSSIAN_KERNELS[2])


def gridear_imagen(img, distancia_pixeles):
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
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not(i % (distancia_pixeles + 1) == 0 or j % (distancia_pixeles + 1) == 0):
                imagen_grideada[i][j] = [0, 0, 0]
    return imagen_grideada
            
def extrae_puntos_grid_imagen(img, distancia_pixeles):
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
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (i % distancia_pixeles == 0 or j % distancia_pixeles == 0):
                LISTA_PUNTOS.append([i,j,img[i][j]])
    return LISTA_PUNTOS
    
io.imsave('mar_grid_20.jpg', gridear_imagen(RGB, 20))
LISTA_PUNTOS = extrae_puntos_grid_imagen(RGB, 30)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
IMAGEN_MALLADA = gridear_imagen(RGB,20)
forma_original = IMAGEN_MALLADA.shape

# Flatten image.
X = np.reshape(IMAGEN_MALLADA, [-1, 3])
bandwidth = estimate_bandwidth(X, quantile=0.1, n_samples=100)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)

labels = ms.labels_
print(labels.shape)
cluster_centers = ms.cluster_centers_
print(cluster_centers.shape)

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

segmented_image = np.reshape(labels, forma_original[:2])  # Just take size, ignore RGB channels.


plt.imshow(segmented_image)

       