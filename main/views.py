from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Bidon, Producto
from .forms import BidonForm, ProductoForm, CategoriaForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

# VIEWS DE PRODUCTOS
def producto_list(request):
    return render(request, 'main/producto/producto_list.html', {'bidones': Bidon.objects.all(),'otros': Producto.objects.all()})

def tienda_view(request):
    return render(request, 'main/producto/producto_catalogo.html', {'bidones': Bidon.objects.all(),'otros': Producto.objects.all()})

def bidon_detail(request, pk):
    bidon = get_object_or_404(Bidon, pk=pk)
    return render(request, 'main/producto/bidon_detail.html', {'bidon': bidon})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'main/producto/producto_detail.html', {'producto': producto})

def producto_create_select(request):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    return render(request, 'main/producto/producto_create_select.html')

def bidon_create(request):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
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
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado con éxito!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al intentar crear el producto. Por favor verifica los datos.')
    return render(request, 'main/producto/producto_create.html', {'form': form})

def bidon_edit(request, pk):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    bidon = get_object_or_404(Bidon, pk=pk)
    form = BidonForm(request.POST or None, request.FILES or None, instance=bidon)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Bidón actualizado con éxito!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al intentar actualizar el bidón. Por favor verifica los datos.')
    return render(request, 'main/producto/bidon_edit.html', {'form': form, 'bidon': bidon})

def producto_edit(request, pk):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado con éxito!')
            return redirect('product_list')
        else:
            messages.error(request, 'Hubo un error al intentar actualizar el producto. Por favor verifica los datos.')
    return render(request, 'main/producto/producto_edit.html', {'form': form, 'producto': producto})

def bidon_delete(request, pk):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    bidon = get_object_or_404(Bidon, pk=pk)
    if request.method == 'POST':
        bidon.delete()
        messages.success(request, '¡Bidón eliminado con éxito!')
        return redirect('product_list')
    return render(request, 'main/producto/producto_delete.html', {'producto': bidon})

def producto_delete(request, pk):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '¡Producto eliminado con éxito!')
        return redirect('product_list')
    return render(request, 'main/producto/producto_delete.html', {'producto': producto})

# VIEWS DE CATEGORIAS

def categoria_create(request):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
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
