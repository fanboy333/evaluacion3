from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear el perfil del usuario directamente con rol CLIENTE
            Profile.objects.create(user=user, role=Profile.Roles.CLIENTE)
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Aguas Don Dino.')
            return redirect('home')
        else:
            messages.error(request, 'Error al registrar. Por favor, verifica los datos.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')

def manage_accounts_view(request):
    # Esto revisa si el usuario está como admin
    if not request.user.is_authenticated or request.user.profile.role != Profile.Roles.ADMINISTRADOR:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
        
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        if user_id and new_role in Profile.Roles.values:
            target_user = get_object_or_404(User, id=user_id)
            target_user.profile.role = new_role
            target_user.profile.save()
            messages.success(request, f'Rol de {target_user.username} actualizado a {target_user.profile.get_role_display()}.')
        return redirect('manage_accounts')
        
    # Get all users (ordered by username)
    users = User.objects.all().select_related('profile').order_by('username')
    roles_choices = Profile.Roles.choices
    return render(request, 'registration/manage_accounts.html', {
        'users': users,
        'roles_choices': roles_choices
    })


