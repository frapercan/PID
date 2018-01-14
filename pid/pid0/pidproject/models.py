from django.db import models

# Create your models here.
class Imagen(models.Model):
    nombre = models.CharField(max_length=200)
    archivo = models.ImageField(upload_to="imagenes")
    formato = models.SlugField()
    editada = models.BooleanField(default=False)

class Prueba(models.Model):
    original = models.ForeignKey('Imagen',on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_original")
    resultado = models.ForeignKey('Imagen',on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_resultado")
