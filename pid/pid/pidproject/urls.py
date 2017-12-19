from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imagenes', views.imagenes, name='imagenes'),
    path('pruebas', views.pruebas, name='pruebas'),
    path('upload', views.upload, name='upload'),
    path('run', views.run, name='run')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
