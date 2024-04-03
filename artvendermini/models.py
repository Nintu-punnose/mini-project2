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
    certificate = models.FileField(upload_to='admin_certificates/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)
    certificate_status = models.CharField(max_length=10,choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
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
    approval_status = models.CharField(max_length=10, choices=[  ('approved', 'Approved'), ('rejected', 'Rejected')], default='approved')
    
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
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

class User_Bid(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_auctions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_auctions', null=True, blank=True)
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name='bids')  # Corrected this line
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_time=models.DateTimeField()
    

    def __str__(self):
        return f"Bid for {self.auction_item.name}"
    
class AuctionListing(models.Model):
    auction_item = models.OneToOneField(AuctionItem, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_listings')
    latest_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    payment_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='Pending')
   
    
class AuctionOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auctionlisting = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True)
    buyer_pincode = models.CharField(max_length=10)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=15)
    buyer_state = models.CharField(max_length=255)
    buyer_city = models.CharField(max_length=255)
    buyer_address = models.TextField()
    buyer_locality = models.CharField(max_length=255)
    buyer_landmark = models.CharField(max_length=255, blank=True, null=True)
    razorpay_id = models.CharField(max_length=255, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='Pending')
    approval_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"Auction Order for {self.auctionlisting.auction_item.name}"
    
class ProductDetails(models.Model):
    auction_order = models.ForeignKey(AuctionOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=10, null=True, default=None)
    date = models.DateField(null=True)
    otp_status = models.CharField(max_length=10, choices=[('failed', 'Failed'), ('sucess', 'Sucess')], default='failed')
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending')
    
    
class AuctionRejectAdmin(models.Model):
    art_id = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    reason = models.TextField()

from django.db import models

class DeliveryRegistration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pin = models.CharField(max_length=10)  # PIN code
    latitude = models.FloatField()  # Latitude
    longitude = models.FloatField()  # Longitude
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255)
    max_delivery_distance = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    approval_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return self.name


class DeliveryProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pin = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    max_delivery_km = models.IntegerField(null=True)
    approval_status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return self.user.username
    
class Rating(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_ratings')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_ratings')
    rating = models.IntegerField()
    def __str__(self):
        return f"Rating from {self.buyer.username} to {self.artist.username}: {self.rating}"





