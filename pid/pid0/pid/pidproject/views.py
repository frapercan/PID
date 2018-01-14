from django.shortcuts import render
from django.http import HttpResponse
from .models import Imagen, Prueba
from .algorithms import prueba1
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    imagenes = Imagen.objects.all()[:3]
    context = {
        'imagenes':imagenes
    }
    return render(request,'pidproject/index.html',context)
    #return HttpResponse("Hello, world. You're at the polls index.")

def imagenes(request):
    imagenes = Imagen.objects.all()
    context = {
        'imagenes':imagenes
    }
    return render(request,'pidproject/imagenes.html',context)

def pruebas(request):
    return render(request,'pidproject/pruebas.html')

def upload(request):
    new_image_file = request.FILES['imageFile']
    new_image_name = "imagen"
    new_image_format = "jpg"
    new_image = Imagen(nombre=new_image_name,archivo=new_image_file,formato=new_image_format)
    new_image.save()
    return render(request,'pidproject/index.html')

def run(request):
    image_pk = request.GET['imagePk']
    image_selected = Imagen.objects.get(pk=image_pk)
    context = {
        'image_url':prueba1(image_selected.archivo.url),
        'image':image_selected
    }
    return render(request,'pidproject/run.html',context)
