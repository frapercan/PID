from PIL import Image, ImageOps
import PIL
from .models import Imagen, Prueba
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
import itertools as it
import mean_shift_epanechnikov as ms
import grid_utils as grid
from tempfile import NamedTemporaryFile
import foreground_estimation as fe
import energy_generation as eg

def call_to_action(image_pk,test_pk,grid_size):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)

    maxsize = (200, 200)

    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    ms_data = grid.puntos_interseccion(np.array(image_for_pil),int(grid_size))
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

def grid_over_image(image_pk,test_pk,grid_size):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_grid = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)
    image_for_grid.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    #ms_data = grid.puntos_interseccion(np.array(image_for_pil),int(grid_size))
    image_for_grid = Image.fromarray(grid.generar_imagen_con_grid(np.array(image_for_grid),int(grid_size)))
    image_for_grid.save("grid_{}.png".format(image_selected.nombre),"png")
    fil = open("grid_{}.png".format(image_selected.nombre), 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre="grid_{}.png".format(image_selected.nombre),archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test = Prueba.objects.get(pk=test_pk)
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url

def meanshift(image_pk,test_pk,grid_size):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)

    maxsize = (200, 200)

    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    ms_data = grid.puntos_interseccion(np.array(image_for_pil),int(grid_size))
    mean_shift = ms.MeanShift(kernel='epanechnikov_kernel')
    mean_shift_result = mean_shift.cluster(ms_data,80,kernel_bandwidth=[255,100])
    original_points =  mean_shift_result.original_points
    shifted_points = mean_shift_result.shifted_points
    cluster_assignments = mean_shift_result.cluster_ids
    original_points_file = open('op.npy','wb+')
    shifted_points_file = open('sp.npy','wb+')
    cluster_assignments_file = open('ca.npy','wb+')
    np.save(original_points_file,original_points)
    np.save(shifted_points_file,shifted_points)
    np.save(cluster_assignments_file,cluster_assignments)
    image_for_grid = Image.fromarray(grid.visualizar_clusteres(np.array(image_for_pil),mean_shift_result)[0])
    original_points_file.close()
    shifted_points_file.close()
    cluster_assignments_file.close()

    image_for_grid.save("ms_{}.png".format(image_selected.nombre),"png")
    fil = open("ms_{}.png".format(image_selected.nombre), 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    fil.close()
    content_file.name="edited.png"
    image_edited = Imagen(nombre="ms_{}.png".format(image_selected.nombre),archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test = Prueba.objects.get(pk=test_pk)
    original_points_file = open('op.npy','rb')
    test.op_file = ContentFile(original_points_file.read())
    original_points_file.close()
    shifted_points_file = open('sp.npy','rb')
    test.sp_file = ContentFile(shifted_points_file.read())
    shifted_points_file.close()
    cluster_assignments_file = open('ca.npy','rb')
    test.ca_file = ContentFile(cluster_assignments_file.read())
    cluster_assignments_file.close()
    test.resultado=image_edited
    print(test.op_file)
    test.save()

    return image_edited.archivo.url

def foreground_estimation(image_pk,test_pk,grid_size):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    test = Prueba.objects.get(pk=test_pk)
    op = np.load(test.op_file)
    sp = np.load(test.sp_file)
    ca = np.load(test.ca_file)
    mean_shift_result = ms.MeanShiftResult(op,sp,ca)
    x_y_c = fe.cambia_formato(mean_shift_result)
    foreground_estimator = fe.foreground_estimation(x_y_c)
    classified = fe.classify_points()
    morf = eg.energy_generation(classified,np.shape(np.array(image_for_pil)),grid_size,nombre_salida="transformacion_distancia.png",nombre_grid_interseccion_figura="grid_interseccion_figura.png",nombre_morfologia="morfologia.png")
    morf.interseccion_grid_figura()
    morf.morfologia()
    morf_img = Image.fromarray(morf.res,'L')
    morf_img.save(morf.nombre_morfologia+"_{}".format(image_selected.nombre),'png')
    fil = open(morf.nombre_morfologia+"_{}".format(image_selected.nombre), 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre=morf.nombre_morfologia+"_{}".format(image_selected.nombre),archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url
