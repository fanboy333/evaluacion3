import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .utils import get_webpay_transaction
from .models import Producto, Pedido, Carrito, ItemCarrito
from .forms import ProductoForm, CategoriaForm

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

# VIEWS DE PRODUCTOS
def producto_list(request):
    return render(request, 'main/producto/producto_list.html', {'productos': Producto.objects.all()})

def tienda_view(request):
    return render(request, 'main/producto/producto_catalogo.html', {'productos': Producto.objects.all()})

def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'main/producto/producto_detail.html', {'producto': producto})

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
            return redirect('producto_create')
        else:
            messages.error(request, 'Hubo un error al intentar crear la categoría. Por favor verifica los datos.')
    return render(request, 'main/categoria/categoria_create.html', {'form': form})

# VIEWS DEL CARRITO

def ver_carrito(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para ver tu carrito.')
        return redirect('login')
        
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    
    for pk, info in carrito.items():
        cantidad = info.get('cantidad', 1)
        
        try:
            producto = Producto.objects.get(pk=pk)
            subtotal = producto.precio * cantidad
            total += subtotal
            
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal,
                'id': pk
            })
        except Producto.DoesNotExist:
            # Si un producto fue borrado de la BD por el admin, lo ignoramos o lo sacamos de la sesión
            pass
        
    cantidad_total = sum(item['cantidad'] for item in items)
        
    return render(request, 'main/carrito/ver_carrito.html', {
        'items': items,
        'total': total,
        'cantidad_total': cantidad_total
    })

def agregar_al_carrito(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar productos al carrito.')
        return redirect('login')
        
    carrito = request.session.get('carrito', {})
    key = str(pk)
    
    producto = get_object_or_404(Producto, pk=pk)
    cantidad_actual = carrito.get(key, {}).get('cantidad', 0)
    
    # ACÁ ESTÁ LA VALIDACION PARA Q NO SE PASE DEL STOCK
    if cantidad_actual + 1 > producto.stock:
        messages.warning(request, f"No queda suficiente stock disponible para '{producto.nombre}'.")
    else:
        if key in carrito:
            carrito[key]['cantidad'] += 1
        else:
            carrito[key] = {
                'id': pk,
                'cantidad': 1
            }
        request.session['carrito'] = carrito
        messages.success(request, f"¡'{producto.nombre}' se agregó al carrito!")
        
    return redirect(request.META.get('HTTP_REFERER', 'tienda'))

def restar_del_carrito(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para modificar el carrito.')
        return redirect('login')
        
    carrito = request.session.get('carrito', {})
    key = str(pk)
    
    if key in carrito:
        if carrito[key]['cantidad'] > 1:
            carrito[key]['cantidad'] -= 1
            messages.success(request, "Cantidad reducida.")
        else:
            del carrito[key]
            messages.success(request, "Producto removido del carrito.")
        request.session['carrito'] = carrito
        
    return redirect('ver_carrito')

def eliminar_del_carrito(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para modificar el carrito.')
        return redirect('login')
        
    carrito = request.session.get('carrito', {})
    key = str(pk)
    
    if key in carrito:
        del carrito[key]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado del carrito.")
        
    return redirect('ver_carrito')

def iniciar_pago(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para proceder al pago.')
        return redirect('login')
        
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('tienda')
        
    total = 0
    for pk, info in carrito.items():
        cantidad = info.get('cantidad', 1)
        try:
            producto = Producto.objects.get(pk=pk)
            total += producto.precio * cantidad
        except Producto.DoesNotExist:
            pass
            
    if total <= 0:
        messages.warning(request, 'El total debe ser mayor a 0.')
        return redirect('ver_carrito')
        
    buy_order = f'orden-{request.user.id}-{random.randint(1000, 9999)}'
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri('/carrito/pago-exitoso/')
    
    try:
        tx = get_webpay_transaction()
        response = tx.create(buy_order=buy_order, session_id=session_id, amount=total, return_url=return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")
    except Exception as e:
        messages.error(request, f'Error al iniciar la transacción con Webpay: {e}')
        return redirect('ver_carrito')

def pago_exitoso(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para ver esta sección.')
        return redirect('login')
        
    token = request.GET.get('token_ws')
    if not token:
        return redirect('ver_carrito')
        
    try:
        tx = get_webpay_transaction()
        response = tx.commit(token) 
        
        if response.get('status') == 'AUTHORIZED':
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            items = carrito.items.all().select_related('producto')
            
            total = response.get('amount')
            for item in items:
                cantidad = item.cantidad
                producto = item.producto
                
                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                else:
                    producto.stock = 0
                producto.save()
            
            Pedido.objects.create(usuario=request.user, total=total, estado='CONF')
            
            # Limpiar los items del carrito en la base de datos
            items.delete()
            
            return render(request, 'main/carrito/pago_exitoso.html', {
                'response': response,
                'monto': response.get('amount')
            })
        else:
            messages.error(request, 'La transacción fue rechazada por el banco emisor.')
            return redirect('ver_carrito')
            
    except Exception as e:
        messages.error(request, f'Error al confirmar la transacción: {e}')
        return redirect('ver_carrito')

def registro_ventas(request):
    if not request.user.is_authenticated or request.user.profile.role != 'ADMIN':
        return redirect('home')
    pedidos = Pedido.objects.all().order_by('-creado_en')
    return render(request, 'main/pedido/registro_ventas.html', {'pedidos': pedidos})
