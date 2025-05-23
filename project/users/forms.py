from django import forms
from django.contrib.auth.forms import AuthenticationForm, \
    UserCreationForm, UserChangeForm
from .models import User
from .models import UserPost


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
        )

        image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*'
        }))



class PostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['title', 'content', 'image']  # Только нужные поля
