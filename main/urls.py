from django.urls import path
from .views import producto_list, producto_delete, bidon_create, home, producto_create_select, producto_create, categoria_create

urlpatterns = [
    # URLS DE PRODUCTOS
    path('', home, name='home'),
    path('productos/list', producto_list, name='product_list'),
    path('productos/create', producto_create_select, name='product_create_select'),
    path('productos/create/bidon', bidon_create, name='bidon_create'),
    path('productos/create/botella', producto_create, name='producto_create'),
    path('productos/delete', producto_delete, name='product_delete'),

    # URLS DE CATEGORIAS
    path('categorias/create', categoria_create, name='categoria_create'),
]
