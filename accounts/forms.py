from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Address


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username',
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
        })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'gender', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+91'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-input'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'address_type', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Address line 2 (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Pincode'}),
            'address_type': forms.Select(attrs={'class': 'form-input'}),
        }
