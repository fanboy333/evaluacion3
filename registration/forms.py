from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Create profile, default role (CLIENTE) will be applied automatically by the model
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = Profile.Roles.CLIENTE
        profile.save()
        return user