from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    class Roles(models.TextChoices):
        ADMINISTRADOR = 'ADMIN', 'Administrador'
        CLIENTE = 'CLIENT', 'Cliente'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENTE)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
