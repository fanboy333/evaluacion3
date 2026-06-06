from django.urls import path, include
from .views import producto_list, producto_delete, producto_create

urlpatterns = [
    # URLS DE PRODUCTOS
    path('', producto_list, name='product_list'),
    path('productos/create', producto_create, name='product_create'),
    path('productos/delete', producto_delete, name='product_delete'),
]
