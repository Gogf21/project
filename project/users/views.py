from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import UserPost
from django.core.paginator import Paginator

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)

            if user:
                auth.login(request, user)
                return redirect('users:profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form':form})

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save() # сохранение юзера в бд
            user = form.instance #Получаем только что созданного юзера
            auth.login(request, user)# Авторизуем его
            messages.success(
                request, f'{user.username}, Successful Registration'
            )
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html')

@login_required
def profile(request):
    user_posts = UserPost.objects.filter(user=request.user)\
                .select_related('user')\
                .only('title', 'content', 'image', 'created_at')\
                .order_by('-created_at')
    paginator = Paginator(user_posts, 6)  # 6 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user,
                        files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
    
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'users/profile.html',{'form':form,
                'page_obj':page_obj})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:login'))