from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = settings.LOGIN_URL
        self.exempt_urls = [self.login_url] + getattr(settings, 'AUTH_EXEMPT_URLS',[]) #Вытаскивается не запрещенные ссылки без логина
    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in self.exempt_urls:
            return redirect(f'{self.login_url}?next={request.path}')
        if request.user.is_authenticated and request.path in [reverse('user:login'), reverse('user:registration')]:
            return redirect('user:profile')
        return self.get_response(request)