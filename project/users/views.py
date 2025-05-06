from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import UserPost
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import PostForm


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
    user_posts = UserPost.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(user_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'users/posts.html', {
            'posts':page_obj.object_list,
            'has_next': page_obj.has_next()
        })

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()  
            print("🛠 Данные формы:", request.POST)
            print("🛠 FILES:", request.FILES)
            
            if 'image' in request.FILES:
                print("✅ Файл сохранён в:", user.image.path)  
                print("✅ URL файла:", user.image.url)  
            
            messages.success(request, 'Profile was changed')
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            print("❌ Ошибки формы:", form.errors)  
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {
        'form': form,
        'posts':page_obj.object_list,
        'has_next':page_obj.has_next()
    })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:login'))


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)