from PIL import Image, ImageOps
from .models import Imagen, Prueba
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
import itertools as it
import mean_shift as ms
from ... import grid_utils as grid

def call_to_action(image_pk,test_pk,grid_size):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)

    ms_data = grid.puntos_interseccion(np.array(image_for_pil),int(grid_size))
    print(len(ms_data))
    mean_shifter = ms.MeanShift(kernel='epanechnikov_kernel')
    mean_shift_result = mean_shifter.cluster(ms_data,kernel_bandwidth=[250,150])
    original_points =  mean_shift_result.original_points
    shifted_points = mean_shift_result.shifted_points
    cluster_assignments = mean_shift_result.cluster_ids
    image_for_pil = Image.fromarray(generar_imagen_con_grid(np.array(image_for_pil),int(grid_size)))
    print(original_points)
    print(shifted_points)
    print(cluster_assignments)

    image_for_pil.save("edited_.png","png")

    fil = open("edited_.png", 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre=image_selected.nombre,archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test = Prueba.objects.get(pk=test_pk)
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url
