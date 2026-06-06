from django.db import models

# Create your models here.
class Producto(models.Model):
    class MaterialSeleccion(models.TextChoices):
        PLASTICO = 'PET', 'Plastico'
        POLICARBONATO = 'POL', 'Policarbonato'
    nombre = models.CharField(max_length=100)
    material = models.CharField(max_length=50, choices=MaterialSeleccion.choices, default=MaterialSeleccion.PLASTICO)
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='producto')