from django.shortcuts import render
from django.http import HttpResponse
from .models import Imagen, Prueba
from .algorithms import call_to_action
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    imagenes = Imagen.objects.filter(editada=False)[:3]
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
    new_test = Prueba(original=image_selected,resultado=image_selected)
    new_test.save()
    context = {
        'image_url':call_to_action(image_pk,new_test.pk,request.GET['gridSize']),
        'image':image_selected
    }
    return render(request,'pidproject/run.html',context)
