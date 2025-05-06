from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('create-post/', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout')
]
