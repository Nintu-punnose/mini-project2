from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    role = models.CharField(max_length=20)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

