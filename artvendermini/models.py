from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    role = models.CharField(max_length=20)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class UploadArtDetail(models.Model):
    art_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255,null=True)
    art_type = models.CharField(max_length=255,null=True)
    size = models.CharField(max_length=50,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    year = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='art_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'bmp'])], blank=True)
    certificate = models.FileField(upload_to='art_certificates/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)
    description = models.TextField()
    approval_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name