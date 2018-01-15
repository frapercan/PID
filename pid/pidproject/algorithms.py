'''
Este módulo contiene todas las funciones necesarias para ejecutar cada paso del algoritmo desde views.py/run
'''


from PIL import Image, ImageOps, ImageFilter
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
import bayesian as bs
import superpixel as spx
import bokeh


def grid_over_image(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_grid = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)
    image_for_grid = image_for_grid.filter(ImageFilter.GaussianBlur(sigma))
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

def meanshift(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    image_for_pil = image_for_pil.filter(ImageFilter.GaussianBlur(sigma))

    maxsize = (200, 200)

    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    ms_data = grid.puntos_interseccion(np.array(image_for_pil),int(grid_size))
    mean_shift = ms.MeanShift(kernel='epanechnikov_kernel')
    mean_shift_result = mean_shift.cluster(ms_data,distance,kernel_bandwidth=[100,255])
    original_points =  mean_shift_result.original_points
    shifted_points = mean_shift_result.shifted_points
    cluster_assignments = mean_shift_result.cluster_ids
    print(cluster_assignments)

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
    cf_op = ContentFile(original_points_file.read())
    cf_op.name="op.npy"
    test.op_file = cf_op
    original_points_file.close()
    shifted_points_file = open('sp.npy','rb')
    cf_sp = ContentFile(shifted_points_file.read())
    cf_sp.name = "sp.npy"
    test.sp_file = cf_sp
    shifted_points_file.close()
    cluster_assignments_file = open('ca.npy','rb')
    cf_ca = ContentFile(cluster_assignments_file.read())
    cf_ca.name = "ca.npy"
    test.ca_file = cf_ca
    cluster_assignments_file.close()
    test.resultado=image_edited
    print(test.op_file)
    test.save()

    return image_edited.archivo.url

def foreground_estimation(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)

    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    test = Prueba.objects.get(pk=test_pk)
    op = np.load(test.op_file)
    sp = np.load(test.sp_file)
    ca = np.load(test.ca_file)
    mean_shift_result = ms.MeanShiftResult(op,sp,ca)

    x_y_c = fe.cambia_formato(mean_shift_result)
    foreground_estimator = fe.foreground_estimation(x_y_c)
    classified = foreground_estimator.classify_points()
    print(classified)
    morf = eg.energy_generation(classified,np.shape(np.array(image_for_pil)),int(grid_size),nombre_salida="transformacion_distancia.png",nombre_grid_interseccion_figura="grid_interseccion_figura.png",nombre_morfologia="morfologia.png")
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

def energy_generation(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)

    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    test = Prueba.objects.get(pk=test_pk)
    op = np.load(test.op_file)
    sp = np.load(test.sp_file)
    ca = np.load(test.ca_file)
    mean_shift_result = ms.MeanShiftResult(op,sp,ca)

    x_y_c = fe.cambia_formato(mean_shift_result)
    foreground_estimator = fe.foreground_estimation(x_y_c)
    classified = foreground_estimator.classify_points()
    print(classified)
    energy = eg.energy_generation(classified,np.shape(np.array(image_for_pil)),int(grid_size),nombre_salida="transformacion_distancia_{}.png".format(image_selected.nombre),nombre_grid_interseccion_figura="grid_interseccion_figura.png",nombre_morfologia="morfologia.png")
    energy_map = energy.hacer_saliency_map()

    fil = open(energy.nombre_salida, 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre=energy.nombre_salida,archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url

# def bayesian(image_pk,test_pk,grid_size,distance,sigma):
#     image_selected = Imagen.objects.get(pk=image_pk)
#     image_for_pil = Image.open("."+image_selected.archivo.url)
#     maxsize = (200, 200)
#
#     image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)
#     test = Prueba.objects.get(pk=test_pk)
#     op = np.load(test.op_file)
#     sp = np.load(test.sp_file)
#     ca = np.load(test.ca_file)
#     mean_shift_result = ms.MeanShiftResult(op,sp,ca)
#
#     new_assignments = bs.reduce_clusters(mean_shift_result,int(grid_size))
#     print(new_assignments)
#     mean_shift_result.cluster_ids=new_assignments
#
#     bayesian = bs.BayesianClassifier(mean_shift_result)
#     bayesian.show_classifiers()
#
#     LISTA_PUNTOS_BAYESIAN=grid.puntos_interseccion(np.array(image_for_pil), 1)
#     bayesian_clustering = bayesian.cluster_data_points(LISTA_PUNTOS_BAYESIAN)
#     bayesian_result = ms.MeanShiftResult(LISTA_PUNTOS_BAYESIAN,np.zeros(1),bayesian_clustering)
#     res_b = grid.visualizar_clusteres(np.array(image_for_pil),bayesian_result)
#     img = Image.fromarray(res_b[0],'RGB')
#     img.save("bayesian_{}.png".format(image_selected.nombre),'png')
#
#     fil = open("bayesian_{}.png".format(image_selected.nombre), 'rb')
#     rd = fil.read()
#     content_file = ContentFile(rd)
#     content_file.name="edited.png"
#     image_edited = Imagen(nombre="bayesian_{}.png".format(image_selected.nombre),archivo=content_file,formato="png",editada=True)
#     image_edited.save()
#     test.resultado=image_edited
#     test.save()
#
#     return image_edited.archivo.url

def superpixel(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)
    thumbnail = grid.thumbnail("."+image_selected.archivo.url,(200,200))
    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)

    test = Prueba.objects.get(pk=test_pk)
    op = np.load(test.op_file)
    sp = np.load(test.sp_file)
    ca = np.load(test.ca_file)
    mean_shift_result = ms.MeanShiftResult(op,sp,ca)

    x_y_c = fe.cambia_formato(mean_shift_result)
    foreground_estimator = fe.foreground_estimation(x_y_c)
    classified = foreground_estimator.classify_points()
    print(classified)
    energy = eg.energy_generation(classified,np.shape(np.array(image_for_pil)),int(grid_size),nombre_salida="transformacion_distancia_{}.png".format(image_selected.nombre),nombre_grid_interseccion_figura="grid_interseccion_figura.png",nombre_morfologia="morfologia.png")
    energy_map = energy.hacer_saliency_map()

    s = spx.superpixel(nombre_thumbnail=thumbnail,profundidad=energy_map,nombre_salida="superpixel_{}.png".format(image_selected.nombre))
    s.hacer_superpixel()

    fil = open(s.nombre_salida, 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre=energy.nombre_salida,archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url

def adaptive_bokeh(image_pk,test_pk,grid_size,distance,sigma):
    image_selected = Imagen.objects.get(pk=image_pk)
    image_for_pil = Image.open("."+image_selected.archivo.url)
    maxsize = (200, 200)
    thumbnail = grid.thumbnail("."+image_selected.archivo.url,(200,200))
    image_for_pil.thumbnail(maxsize, PIL.Image.ANTIALIAS)

    test = Prueba.objects.get(pk=test_pk)

    d = bokeh.bokeh("."+image_selected.archivo.url,thumbnail,"superpixel_{}.png".format(image_selected.nombre))
    d.difuminacion_gaussiana_fondo()

    fil = open("gauss_adaptativo.png", 'rb')
    rd = fil.read()
    content_file = ContentFile(rd)
    content_file.name="edited.png"
    image_edited = Imagen(nombre="gauss_adaptativo{}.png".format(image_selected.nombre),archivo=content_file,formato="png",editada=True)
    image_edited.save()
    test.resultado=image_edited
    test.save()

    return image_edited.archivo.url
