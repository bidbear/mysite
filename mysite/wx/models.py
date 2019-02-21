from django.db import models

# Create your models here.
class Wx_Access_Token(models.Model):
    """docstring for Wx_Access_Token"""
    access_token = models.CharField(max_length=1024)
    once_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.access_token