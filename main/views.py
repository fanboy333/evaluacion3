from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

# Create your views here.

# VIEWS DE PRODUCTOS
def producto_list(request):
    return render(request, 'main/producto/producto_list.html', {'productos': Producto.objects.all()})

def producto_create(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('prodicto_list')
    return render(request, 'main/producto/producto_create.html', {'form': form})

def producto_delete(request):
    return render(request, 'main/producto/producto_delete.html')


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
