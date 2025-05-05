from django.db import models
from django.contrib.auth.models import AbstractUser
import os
class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True, null=True)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        try:
            old_user = User.objects.get(pk=self.pk)
            if old_user.image and old_user.image != self.image:
                if os.path.isfile(old_user.image.path):
                    os.remove(old_user.image.path)
        except User.DoesNotExist:
            pass
            
        super().save(*args, **kwargs)
    
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

