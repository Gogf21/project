from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
    
class UserPost(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/%Y/%m/%d',blank=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

