from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UserChangeForm
from .models import User


class UserLoginForm(AuthenticationForm):


    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password1',
            'password2',
        )


        email = forms.EmailField(required=True)


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'image',
            'username',
            'email',
        )

        image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }))

