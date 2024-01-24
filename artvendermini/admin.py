from django.contrib import admin
from .models import UploadArtDetail,SellerProfile,UserData,Cart,CartItem,ProductSize,ProductType,Order
# Register your models here.

admin.site.register(UploadArtDetail)
admin.site.register(UserData)
admin.site.register(SellerProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ProductSize)
admin.site.register(ProductType)
admin.site.register(Order)
