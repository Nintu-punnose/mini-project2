from django.contrib import admin
from .models import UploadArtDetail,SellerProfile,UserData
# Register your models here.

admin.site.register(UploadArtDetail)
admin.site.register(UserData)
admin.site.register(SellerProfile)
