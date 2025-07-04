from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .widgets import CustomClearableFileInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2']

    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'birth_date', 'profile_picture']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': CustomClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
