from django.urls import path
from .views import producto_list, producto_delete, bidon_create, home, producto_create_select

urlpatterns = [
    # URLS DE PRODUCTOS
    path('', home, name='home'),
    path('productos/list', producto_list, name='product_list'),
    path('productos/create', producto_create_select, name='product_create_select'),
    path('productos/bidon/create', bidon_create, name='bidon_create'),
    path('productos/delete', producto_delete, name='product_delete'),
]
