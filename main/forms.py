from django import forms
from .models import Bidon, Categoria, Producto

class BidonForm(forms.ModelForm):
    class Meta:
        model = Bidon
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
