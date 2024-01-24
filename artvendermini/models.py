from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid
from django.utils import timezone
from platformdirs import user_data_dir

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    role = models.CharField(max_length=20)
    number = models.CharField(max_length=20,null=True)

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
    

class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    userdata = models.ForeignKey(UserData, on_delete=models.CASCADE, null=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    image = models.ImageField(upload_to='seller_profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class ProductType(models.Model):
    nametype = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    namesize = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

# cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(UploadArtDetail, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    art = models.ForeignKey(UploadArtDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    shipping_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

# views.py




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    product_names = models.CharField(max_length=200)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, default='your_default_value_here')
    razorpay_order_id = models.CharField(max_length=100, default='your_default_value_here')

class artOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    product_names = models.CharField(max_length=200)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, default='your_default_value_here')
    razorpay_order_id = models.CharField(max_length=100, default='your_default_value_here')




from django.db import models

class AuctionItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class User_Bid(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_auctions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_auctions', null=True, blank=True)
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='bids')  # Corrected this line
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bid for {self.auction_item.name}"













