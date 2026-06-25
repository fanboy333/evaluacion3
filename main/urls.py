from django.urls import path
from .views import (
    producto_list, producto_delete, bidon_create, home, 
    producto_create_select, producto_create, categoria_create, 
    tienda_view, bidon_edit, producto_edit, bidon_delete,
    bidon_detail, producto_detail
)

urlpatterns = [
    # URLS DE PRODUCTOS
    path('', home, name='home'),
    path('tienda/', tienda_view, name='tienda'),
    path('tienda/bidon/<int:pk>/', bidon_detail, name='bidon_detail'),
    path('tienda/producto/<int:pk>/', producto_detail, name='producto_detail'),
    path('productos/list', producto_list, name='product_list'),
    path('productos/create', producto_create_select, name='product_create_select'),
    path('productos/create/bidon', bidon_create, name='bidon_create'),
    path('productos/create/botella', producto_create, name='producto_create'),
    # URLS DE EDICION Y ELIMINACION DE LOS PRODUCTITOS 
    path('productos/edit/bidon/<int:pk>/', bidon_edit, name='bidon_edit'),
    path('productos/edit/botella/<int:pk>/', producto_edit, name='producto_edit'),
    path('productos/delete/bidon/<int:pk>/', bidon_delete, name='bidon_delete'),
    path('productos/delete/botella/<int:pk>/', producto_delete, name='producto_delete'),

    # URLS DE CATEGORIAS
    path('categorias/create', categoria_create, name='categoria_create'),
]
