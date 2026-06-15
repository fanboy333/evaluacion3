from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Bidon(models.Model):
    class MaterialSeleccion(models.TextChoices):
        PLASTICO = 'PET', 'Plastico'
        POLICARBONATO = 'POL', 'Policarbonato'
    class RetornableSeleccion(models.TextChoices):
        RETORNABLE = 'RET', 'Retornable'
        NO_RETORNABLE = 'NO_RET', 'No Retornable'
    nombre = models.CharField(max_length=100)
    material = models.CharField(max_length=50, choices=MaterialSeleccion.choices, default=MaterialSeleccion.PLASTICO)
    retornable = models.CharField(max_length=10, choices=RetornableSeleccion.choices, default=RetornableSeleccion.RETORNABLE)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='producto')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='producto')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


