from django.urls import path
from .views import (
    home, tienda_view, producto_detail, producto_list, 
    producto_create, producto_edit, producto_delete,
    categoria_create, ver_carrito, agregar_al_carrito, 
    restar_del_carrito, eliminar_del_carrito,
    iniciar_pago, pago_exitoso, registro_ventas
)

urlpatterns = [
    # URLS DE PRODUCTOS
    path('', home, name='home'),
    path('tienda/', tienda_view, name='tienda'),
    path('tienda/producto/<int:pk>/', producto_detail, name='producto_detail'),
    path('productos/list', producto_list, name='product_list'),
    path('productos/create', producto_create, name='producto_create'),
    path('productos/edit/<int:pk>/', producto_edit, name='producto_edit'),
    path('productos/delete/<int:pk>/', producto_delete, name='producto_delete'),

    # URLS DE CATEGORIAS
    path('categorias/create', categoria_create, name='categoria_create'),

    # URLS DE CARRITO
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:pk>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/restar/<int:pk>/', restar_del_carrito, name='restar_del_carrito'),
    path('carrito/eliminar/<int:pk>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # URLS DE WEBPAY
    path('carrito/pagar/', iniciar_pago, name='iniciar_pago'),
    path('carrito/pago-exitoso/', pago_exitoso, name='pago_exitoso'),
    path('panel-admin/ventas/', registro_ventas, name='registro_ventas'),
]
