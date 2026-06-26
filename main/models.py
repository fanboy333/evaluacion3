from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    class MaterialSeleccion(models.TextChoices):
        PLASTICO = 'PET', 'Plástico'
        POLICARBONATO = 'POL', 'Policarbonato'
        NO_APLICA = 'N/A', 'No aplica'
    class RetornableSeleccion(models.TextChoices):
        RETORNABLE = 'RET', 'Retornable'
        NO_RETORNABLE = 'NO_RET', 'No Retornable'
        NO_APLICA = 'N/A', 'No aplica'

    nombre = models.CharField(max_length=100)
    material = models.CharField(max_length=50, choices=MaterialSeleccion.choices, default=MaterialSeleccion.NO_APLICA)
    retornable = models.CharField(max_length=10, choices=RetornableSeleccion.choices, default=RetornableSeleccion.NO_APLICA)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='producto')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, default='CONF')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} - ${self.total}"

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Carrito de {self.carrito.usuario.username}"



