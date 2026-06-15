from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Bidon
from .forms import BidonForm, ProductoForm, CategoriaForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

# VIEWS DE PRODUCTOS
def producto_list(request):
    return render(request, 'main/producto/producto_list.html', {'productos': Bidon.objects.all()})

def producto_create_select(request):
    return render(request, 'main/producto/producto_create_select.html')

def bidon_create(request):
    form = BidonForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Bidón creado con éxito!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al intentar crear el bidón. Por favor verifica los datos.')
    return render(request, 'main/producto/bidon_create.html', {'form': form})

def producto_create(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado con éxito!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al intentar crear el producto. Por favor verifica los datos.')
    return render(request, 'main/producto/producto_create.html', {'form': form})

def producto_delete(request):
    return render(request, 'main/producto/producto_delete.html')

# VIEWS DE CATEGORIAS

def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría creada con éxito!')
            return redirect('product_create_select')
        else:
            messages.error(request, 'Hubo un error al intentar crear la categoría. Por favor verifica los datos.')
    return render(request, 'main/categoria/categoria_create.html', {'form': form})

# VIEWS DE PEDIDOS
def pedidos_list(request):
    return render(request, 'main/pedidos/pedidos_list.html')

def pedidos_create(request):
    return render(request, 'main/pedidos/pedidos_create.html')

def pedidos_cancel(request):
    return render(request, 'main/pedidos/pedidos_cancel.html')


# VIEWS DEL CARRITO KUN

def ver_carrito(request):
    return render(request, 'main/carrito/ver_carrito.html')
