from django.urls import path
from .views import login_view, register_view, logout_view, manage_accounts_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('manage/', manage_accounts_view, name='manage_accounts'),
]
