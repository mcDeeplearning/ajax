from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})