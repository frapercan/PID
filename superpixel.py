# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 04:18:33 2018

PID
"""

from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)

image = img_as_float(io.imread("jakob-nielsen-thumbs-up.jpg"))


segmentos = slic(image, n_segments = 40, sigma = 10, )

fig = plt.figure("aaaaa")
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mark_boundaries(image, segmentos))
print(segmentos)
plt.show()
