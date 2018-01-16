from django.shortcuts import render
from django.http import HttpResponse
from .models import Imagen, Prueba
from .algorithms import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
PASOS_ALGORITMO={1:grid_over_image,2:meanshift,3:foreground_estimation,4:energy_generation,5:superpixel,6:adaptive_bokeh}
TITULOS_PASOS={1:"Superposición del grid sobre la imagen",2:"Algoritmo MeanShift",3:"Foreground estimation",4:"Mapa de energía",
                5:"Generación del superpixel",6:"Simulación del efecto bokeh"}


def index(request):
    imagenes = Imagen.objects.filter(editada=False)
    context = {
        'imagenes':imagenes
    }
    return render(request,'pidproject/index.html',context)
    #return HttpResponse("Hello, world. You're at the polls index.")

def imagenes(request):
    imagenes = Imagen.objects.filter(editada=False)
    context = {
        'imagenes':imagenes
    }
    return render(request,'pidproject/imagenes.html',context)

def pruebas(request):
    pruebas = Prueba.objects.all()
    context = {
        'pruebas':pruebas
    }
    return render(request,'pidproject/pruebas.html',context)

def upload(request):
    new_image_file = request.FILES['imageFile']
    new_image_name = new_image_file.name
    new_image_format = "jpg"
    new_image = Imagen(nombre=new_image_name,archivo=new_image_file,formato=new_image_format)
    new_image.save()
    return index(request)

def run(request):
    image_pk = request.GET['imagePk']
    image_selected = Imagen.objects.get(pk=image_pk)
    if(int(request.GET['paso'])>6):
        test = Prueba.objects.get(pk=request.GET['test_pk'])
        test.comentario=request.GET['comment']
        test.save()
        pruebas = Prueba.objects.all()
        context = {
            'pruebas':pruebas
        }
        return render(request,'pidproject/pruebas.html',context)
    if('test_pk' not in request.GET):
        test = Prueba(original=image_selected,resultado=image_selected)
        test.save()
    else:
        test = Prueba.objects.get(pk=request.GET['test_pk'])
    context = {
        'image_url':PASOS_ALGORITMO[int(request.GET['paso'])](image_pk,test.pk,request.GET['gridSize'],int(request.GET['distance']),int(request.GET['sigma'])),
        'image':image_selected,
        'image_pk':request.GET['imagePk'],
        'test_pk':test.pk,
        'paso':int(request.GET['paso']),
        'paso_next':int(request.GET['paso'])+1,
        'progress_percent':(int(request.GET['paso'])/6)*100,
        'titulo':TITULOS_PASOS[int(request.GET['paso'])],
        'grid_size':request.GET['gridSize'],
        'distance':request.GET['distance'],
        'sigma':request.GET['sigma']
    }
    return render(request,'pidproject/run.html',context)
