from telnetlib import AUTHENTICATION
from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import AuctionOrder, AuctionRejectAdmin, DeliveryProfile, DeliveryRegistration, ProductDetails, User_Bid, UserData, artOrder,AuctionItem
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UploadArtDetail,SellerProfile
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        number = request.POST['number']
        email = request.POST['email']
        role = request.POST['role']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request, "username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create UserData associated with the user
        userdata = UserData(user=user, role=role, number=number)
        userdata.save()

        return redirect('login')  # Redirect to your login view
    else:
        return render(request, 'signup.html')
    

from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:  # Check if both fields are non-empty
            user = authenticate(username=username, password=password)
        
            if user is not None:
                auth_login(request, user)
                to_role=UserData.objects.get(user_id=request.user.id)
                if to_role.role=='Artist':
                    return redirect('Artist_view')
                elif to_role.role=='customer':
                    return redirect('index')
                elif to_role.role=='Admin':
                    return redirect('admin_pannel')
                else:
                    try:
                        delivary_registration=DeliveryRegistration.objects.get(user_id=request.user.id)
                        if delivary_registration.approval_status == 'Approved':
                            return redirect('delivary_dashboard')
                        elif delivary_registration.approval_status == 'Pending':
                            messages.info(request, "Not Approved by admin..please wait.")
                        else:
                            messages.info(request, "Rejected by admin.")
                    except ObjectDoesNotExist:
                            return redirect('delivary_profile')
                            
            else:
                # Display error message using messages framework
                messages.info(request, "Invalid credentials. Please try again.")
        else:
            # Display error message using messages framework
            messages.info(request, "Please provide both username and password.")

    return render(request, 'login.html')


# def Artist_view(request):
#     return render(request,"Artist_view.html")


from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    print(123)
    logout(request)
    return redirect('login')


def upload_art(request):
    if request.method == 'POST':
        name = request.POST.get('uploadArt_name')
        art_type = request.POST.get('uploadArt_type')
        size = request.POST.get('uploadArt_size')
        price = request.POST.get('uploadArt_price')
        year = request.POST.get('uploadArt_year')
        image = request.FILES.get('uploadArt_image')
        certificate = request.FILES.get('uploadArt_certificate')
        description = request.POST.get('uploadArt_description')
        
        # Create and save the art detail to the database
        art = UploadArtDetail(
            name=name,
            art_type=art_type,
            size=size,
            price=price,
            year=year,
            image=image,
            certificate=certificate,
            description=description,
            user_id=request.user.id
        )
        art.save()
        return redirect('Artist_view')

        # return redirect('art_gallery')  # Redirect to a success page or gallery page
    else:
        messages.info(request, "Please fill all field.")

    return render(request, 'Artist_view.html')  # Render the upload form page for GET request



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Artist_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # art1 =  UploadArtDetail.objects.filter(user_id=request.user.id)
    total_arts_uploaded = UploadArtDetail.objects.filter(user_id=request.user.id).count()
    arts_approved = UploadArtDetail.objects.filter(user_id=request.user.id,approval_status='approved').count()
    artdata = UploadArtDetail.objects.filter(user_id=request.user.id )
    arttype = ProductType.objects.all()
    artsize = ProductSize.objects.all()
    img = SellerProfile.objects.filter(user_id=request.user.id)
    return render(request, "Artist_view.html", {'artdata': artdata,'total':total_arts_uploaded,'art':arts_approved, 'arttype':arttype, 'artsize':artsize, 'img':img})

@login_required
def index(request):
    artdata = UploadArtDetail.objects.filter(approval_status='approved')
    return render(request, "index.html", {'artdata': artdata})


# def admin_pannel(request):
#     if request.method == 'POST':
#         art_id = request.POST.get('art_id')
#         approval_status = request.POST.get('approval_status')

#         try:
#             art = UploadArtDetail.objects.get(id=art_id)
#             art.approval_status = approval_status
#             art.is_approved = (approval_status == 'approved')  # Set is_approved based on approval_status
#             art.save()
#             return redirect('admin_pannel')
#         except UploadArtDetail.DoesNotExist:
#             return HttpResponse("Art not found.")

#     # Retrieve all art data for display in the table
#     art_data = UploadArtDetail.objects.all()
#     return render(request, 'admin_pannel.html', {'art_data': art_data})


from django.db.models import Count

def admin_pannel(request):
    if request.method == 'POST':
        art_id = request.POST.get('art_id')
        approval_status = request.POST.get('approval_status')
        

        try:
            art = UploadArtDetail.objects.get(id=art_id)
            
            art.approval_status = approval_status
            art.is_approved = (approval_status == 'approved')
            art.save()
            return redirect('admin_pannel')
        except UploadArtDetail.DoesNotExist:
            return HttpResponse("Art not found.")

    # Retrieve all art data for display in the table
    art_data = UploadArtDetail.objects.all()

    # Count the total number of arts uploaded
    total_arts_uploaded = art_data.count()

    # Count the number of approved arts
    approved_arts_count = art_data.filter(approval_status='approved').count()

    # Count the total number of users
    total_users = User.objects.count()
    
    # Count the total number of Artist
    total_Artist = UserData.objects.filter(role='Artist').count()

    arttype=ProductType.objects.all()
    artsize=ProductSize.objects.all()
  
    return render(request, 'admin_pannel.html', {
        'art_data': art_data,
        'total_arts_uploaded': total_arts_uploaded,
        'approved_arts_count': approved_arts_count,
        'total_users': total_users,
        'arttype':arttype,
        'artsize':artsize,
        'totalArtist':total_Artist,
    })

# from django.shortcuts import render, redirect, HttpResponse
# from .models import UploadArtDetail, User, UserData, ProductType, ProductSize

# def admin_pannel(request):
#     if request.method == 'POST':
#         art_id = request.POST.get('art_id')
#         approval_status = request.POST.get('approval_status')
        
#         try:
#             art = UploadArtDetail.objects.get(id=art_id)
            
#             art.approval_status = approval_status
#             art.is_approved = (approval_status == 'approved')
#             art.save()
#             return redirect('admin_pannel')  # Redirect to the admin panel page after the update
#         except UploadArtDetail.DoesNotExist:
#             return HttpResponse("Art not found.")

#     # Retrieve all art data for display in the table
#     art_data = UploadArtDetail.objects.all()

#     # Count the total number of arts uploaded
#     total_arts_uploaded = art_data.count()

#     # Count the number of approved arts
#     approved_arts_count = art_data.filter(approval_status='approved').count()

#     # Count the total number of users
#     total_users = User.objects.count()
    
#     # Count the total number of Artist
#     total_Artist = UserData.objects.filter(role='Artist').count()

#     arttype = ProductType.objects.all()
#     artsize = ProductSize.objects.all()
  
#     return render(request, 'admin_pannel.html', {
#         'art_data': art_data,
#         'total_arts_uploaded': total_arts_uploaded,
#         'approved_arts_count': approved_arts_count,
#         'total_users': total_users,
#         'arttype': arttype,
#         'artsize': artsize,
#         'totalArtist': total_Artist,
#     })



from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadArtDetail

def update_art(request, art_id):
    art = get_object_or_404(UploadArtDetail, id=art_id)
    img = SellerProfile.objects.filter(user_id=request.user.id)
    arttype=ProductType.objects.all()
    artsize=ProductSize.objects.all()
    
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('uploadArt_name')
        art_type = request.POST.get('uploadArt_type')
        size = request.POST.get('uploadArt_size')
        price = request.POST.get('uploadArt_price')
        year = request.POST.get('uploadArt_year')
        image = request.FILES.get('uploadArt_image')
        certificate = request.FILES.get('uploadArt_certificate')
        description = request.POST.get('uploadArt_description')

        # Update the art object with the new data
        art.name = name
        art.art_type = art_type
        art.size = size
        art.price = price
        art.year = year

        if image:
            art.image = image

        if certificate:
            art.certificate = certificate

        art.description = description

        # Save the updated art object
        art.save()

        # Redirect to the Artist view or any other page you prefer
        return redirect('Artist_view')
    else:
        # Render the update form with the art details
        return render(request, 'update_art.html', {'art': art, 'is_approved': art.is_approved, 'img':img, 'arttype':arttype, 'artsize':artsize})
    



def delete_art(request, art_id):
    art = get_object_or_404(UploadArtDetail, id=art_id)

    # Check if the user trying to delete the art is the owner (optional)
    if request.user == art.user:
        # Delete the art object from the database
        art.delete()
        return redirect('Artist_view')
    else:
        return HttpResponse("You don't have permission to delete this art")
    

def seller_profile(request):
    user=User.objects.filter(id=request.user.id)
    userdata=UserData.objects.filter(user_id=request.user.id)
    img=SellerProfile.objects.filter(user_id=request.user.id)
    userexists=SellerProfile.objects.filter(user_id=request.user.id).exists()
    if userexists:
        seller=SellerProfile.objects.filter(user_id=request.user.id)
    else:
        seller=None
        print(seller)
    if request.method=='POST':
        phone=request.POST.get('seller-number')
        userdata1=UserData.objects.get(user_id=request.user.id)
        userdata1.number=phone
        userdata1.save()
        if userexists:
            seller1=SellerProfile.objects.get(user_id=request.user.id)
            seller1.district=request.POST.get('seller-district')
            seller1.state=request.POST.get('seller-state')
            seller1.country=request.POST.get('seller-country')
            seller1.address=request.POST.get('seller-address')
            seller1.pincode=request.POST.get('seller-pincode')
            image=request.FILES.get('seller-image')
            if image==None:
                seller1.image=seller1.image
            else:
                seller1.image=image
            seller1.save()
            return redirect('seller_profile')
        else:
            user1=SellerProfile(
            district=request.POST.get('seller-district'),
            state=request.POST.get('seller-state'),
            country=request.POST.get('seller-country'),
            address=request.POST.get('seller-address'),
            pincode=request.POST.get('seller-pincode'),
            image=request.FILES.get('seller-image'),
            user_id=request.user.id,
            )
            user1.save()
            return redirect('seller_profile')
    return render(request,'seller_profile.html',{'user':user,'userdata':userdata,'seller':seller,'img':img})



def images(request):
    images=UploadArtDetail.objects.filter(approval_status='approved')
    return render(request,'images.html',{'images':images})

def image_detail(request,id):
    img_id = get_object_or_404(UploadArtDetail, id=id)
    return render(request,'image_detail.html',{'img_id':img_id})

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')



def Artist(request):
    artistdata1=User.objects.all()
    artistdata2=SellerProfile.objects.all()
    artistdata3=UserData.objects.filter(role='Artist')
    return render(request,'Artist.html',{'artistdata1':artistdata1,'artistdata2':artistdata2,'artistdata3':artistdata3})

from django.shortcuts import render, get_object_or_404
from .models import SellerProfile, UploadArtDetail

def Artist_detail(request, id):
    profile = get_object_or_404(SellerProfile, user_id=id)
    artist_images = UploadArtDetail.objects.filter(user=profile.user, approval_status='approved')
    return render(request, 'Artist_detail.html', {'profile': profile, 'artist_images': artist_images})

    

# cart

from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadArtDetail, Cart, CartItem

def add_to_cart(request, art_id):
    art = get_object_or_404(UploadArtDetail, id=art_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item = CartItem.objects.filter(cart=cart, art=art).first()

    if cart_item:
        # If the item is already in the cart, don't create a new one, and set the quantity to 1
        cart_item.quantity = 1
        cart_item.save()
    else:
        # If the item is not in the cart, create a new cart item with a quantity of 1
        cart_item = CartItem(cart=cart, art=art, quantity=1)
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, art_id):
    art = get_object_or_404(UploadArtDetail, id=art_id)
    cart_item = CartItem.objects.get(cart__user=request.user, art=art)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})


# addtype


from django.shortcuts import render, redirect
from .models import ProductType  # Import your ProductType model

def addtype(request):
    if request.method == 'POST':
        nametype = request.POST.get('nametype')

        product_type=ProductType(nametype=nametype)
        product_type.save()
        return redirect('admin_pannel')  # Redirect to the admin dashboard or any other page
    
    return render(request, 'admin_pannel.html')  # Render the form page for GET requests


# artsize

from django.shortcuts import render, redirect
from .models import ProductSize  # Import your ProductType model

def addsize(request):
    if request.method == 'POST':
        namesize = request.POST.get('namesize')

        product_size=ProductSize(namesize=namesize)
        product_size.save()
        return redirect('admin_pannel')  # Redirect to the admin dashboard or any other page
    
    return render(request, 'admin_pannel.html')  # Render the form page for GET requests

from django.shortcuts import redirect, get_object_or_404
from .models import ProductType, ProductSize

def delete_art_type(request, type_id):
    art_type = get_object_or_404(ProductType, id=type_id)
    art_type.delete()
    return redirect('admin_pannel')

def delete_art_size(request, size_id):
    art_size = get_object_or_404(ProductSize, id=size_id)
    art_size.delete()
    return redirect('admin_pannel')


#email
from django.core.mail import send_mail
from django.conf import settings

def email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        query = request.POST['query']

        message = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nQuery: {query}"

        send_mail(
            'Art Inquiry',  # Subject
            message,  # Message
            email,  # From email address (sender)
            ['artvendor8@gmail.com'],  # List of recipient email addresses
            fail_silently=False
        )

    return render(request, 'email.html')


def alluser(request):
   user = User.objects.all()
   approve_count = UploadArtDetail.objects.filter(user_id=request.user.id).count()
   return render(request, 'alluser.html', {'user': user, 'approve_count': approve_count})



from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Order, Cart, CartItem
from decimal import Decimal
from datetime import datetime, timezone
from razorpay import Client
from django.conf import settings

razorpay_key_id = settings.RAZOR_KEY_ID
razorpay_key_secret = settings.RAZOR_KEY_SECRET

razorpay_client = Client(auth=(razorpay_key_id, razorpay_key_secret))

def payment(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_cost = sum(item.quantity * item.art.price for item in cart_items)
    total_amount = Decimal(str(total_cost)) + Decimal('40.00')

    return render(request, 'payment.html', {'total_amount': total_amount, 'razorpay_merchant_key': razorpay_key_id, 'razorpay_amount': int(total_amount * 100), 'currency': 'INR'})


from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Order, Cart, CartItem
from decimal import Decimal
from datetime import datetime
from django.conf import settings

razorpay_key_id = settings.RAZOR_KEY_ID
razorpay_key_secret = settings.RAZOR_KEY_SECRET

razorpay_client = Client(auth=(razorpay_key_id, razorpay_key_secret))

def paymenthandler(request):
    if request.method == "POST":
        order = artOrder()  # Use the artOrder model

        # Simulate a successful payment
        payment_id = 'dummy_payment_id'
        razorpay_order_id = 'dummy_order_id'

        # Retrieve the cart items for the user
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Calculate the total cost of the cart items
        total_cost = sum(item.quantity * item.art.price for item in cart_items)
        shipping_charge = Decimal('40.00')
        total_amount = total_cost + shipping_charge

        # Get the product names from cart items
        product_names = ", ".join([item.art.name for item in cart_items])

        # Save the order data in the database

        order = artOrder(
            user=request.user,
            order_date=datetime.now(timezone.utc),  # Use timezone.utc for timezone aware datetime
            product_names=product_names,
            total_cost=total_cost,
            shipping_charge=shipping_charge,
            total_amount=total_amount,
            payment_id=payment_id,  # Store the payment ID
            razorpay_order_id=razorpay_order_id  # Store the Razorpay order ID
        )
 
        order.save()

        cart_items.delete()
        # Update the order status or perform any additional actions here

        return render(request, 'cart.html', {'orders': order})  # Render the success page on successful capture of payment
    return HttpResponseBadRequest("Invalid Request")

from .models import Order

def orders(request):
    orders = AuctionOrder.objects.filter(user=request.user)
    return render(request, "orders.html", {'orders': orders})


from django.contrib.auth.decorators import login_required

@login_required
def auction_uploadform(request):
    img = SellerProfile.objects.filter(user_id=request.user.id)
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    if request.method == 'POST':
        name = request.POST.get('name')
        price_range_min = request.POST.get('priceRangeMin')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        # Set the user field with the current user
        auction = AuctionItem(
            user=request.user,
            name=name,
            price_range_min=price_range_min,
            description=description,
            image=image,
            start_date=start_date,
            end_date=end_date
        )
        auction.save()
        return redirect('auction_uploadform')

    return render(request, 'auction_uploadform.html',{'img':img,'current_date_ist':current_date_ist})


from django.shortcuts import render
from django.utils import timezone
from .models import AuctionItem

def auction(request):
    # Get all auction items
    auction_items = AuctionItem.objects.all()

    # Check and update is_active for auctions that have ended
    for auction_item in auction_items:
    # Convert end_date to the local timezone
        end_date_local = timezone.localtime(auction_item.end_date)
        end_time_local = end_date_local.time()
        

    # Check if end_date is in the past
        print(end_time_local,datetime.now().time())
        if end_time_local < datetime.now().time():
            auction_item.is_active = False
            auction_item.save() 

    # Get the remaining active auction items
    updated_auction_items = AuctionItem.objects.filter(is_active=True,status=True)

    return render(request, 'auction.html', {'auction_items': updated_auction_items})


from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from .models import AuctionItem, User_Bid

def auction_bid(request, auction_id):
    auction_details = get_object_or_404(AuctionItem, id=auction_id)

    # Set default values for seller and buyer
    seller = User.objects.get(id=auction_details.user_id)
    buyer = None
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    print(current_date_ist)

    if request.method == 'POST':
        # Get the bid_price from the form
        bid_price = request.POST.get('bid_price')

        # Set buyer to the logged-in user
        buyer = request.user
       
        bid = User_Bid( 
            seller=seller,
            buyer=buyer,
            auction_item=auction_details,
            bid_price=bid_price,
            current_time = current_date_ist
        )

        bid.save()

        return redirect('auction_bid', auction_id=auction_id)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        highest_bid = User_Bid.objects.filter(auction_item=auction_details).aggregate(Max('bid_price'))['bid_price__max']
        data = {
            'highest_bid': highest_bid,
        }
        return JsonResponse(data)
    
    highest_bid = User_Bid.objects.filter(auction_item=auction_details).aggregate(Max('bid_price'))['bid_price__max']

    # Render the template without 'name' when it's not defined
    return render(request, 'auction_bid.html', {'auction_details': auction_details, 'seller': seller, 'buyer': buyer,'current_date': current_date_ist, 'highest_bid': highest_bid})



import pytz
@login_required
def artist_uploaded_auction(request):
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    auction_details = AuctionItem.objects.filter(user_id=request.user.id)
    img = SellerProfile.objects.filter(user_id=request.user.id)
    reason = AuctionRejectAdmin.objects.filter(seller=request.user.id)
    return render(request, 'artist_uploaded_auction.html', {'auction_details': auction_details, 'current_date': current_date_ist,'img':img,'reason':reason})


from django.db import IntegrityError

def artist_auction_view(request, art_id):
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    admin_buyer_shown = User_Bid.objects.filter(auction_item_id=art_id).order_by('-bid_price')[:1]
    img = SellerProfile.objects.filter(user_id=request.user.id)
    print(current_date_ist)

    auction_item = get_object_or_404(AuctionItem, pk=art_id,is_active=True)
    end_date = auction_item.end_date

    # Check if the current time is greater than or equal to the end date
    if current_date_ist >= end_date:
        bid = User_Bid.objects.get(auction_item__id=art_id)
        auction_listing = AuctionListing.objects.create(
            auction_item=bid.auction_item,
            buyer=bid.buyer,
            seller=bid.seller,
            latest_price=bid.bid_price,
            end_date=bid.auction_item.end_date,
        )
        auction_listing.save()

    return render(request, 'artist_auction_view.html', {'admin_buyer_shown': admin_buyer_shown, 'art_id': art_id,'current_date_ist':current_date_ist,'img':img})



def artist_auction_view_all(request,bid_id):
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    admin_buyer_shown = User_Bid.objects.filter(auction_item_id=bid_id)
    img = SellerProfile.objects.filter(user_id=request.user.id)
    return render(request, 'artist_auction_view_all.html', {'admin_buyer_shown': admin_buyer_shown,'current_date_ist':current_date_ist,'img':img})


# def notification(request):
#     return render(request,'notification.html') 



# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import AuctionItem

def update_auction(request):
    if request.method == "POST":
        auction_id = request.POST.get("editAuctionId")
        auction_name = request.POST.get("editAuctionName")
        end_date = request.POST.get("editEndDate")
        price = request.POST.get("editPrice")

        # Update the auction item in the database
        try:
            auction = AuctionItem.objects.get(pk=auction_id)
            auction.name = auction_name
            auction.end_date = end_date
            auction.price_range_min = price
            auction.save()
            return redirect('artist_uploaded_auction')
        except AuctionItem.DoesNotExist:
            return HttpResponse("Auction item not found", status=404)

    return HttpResponse("Invalid request method", status=400)


# views.py

def delete_auction(request):
    if request.method == 'GET':
        auction_id = request.GET.get('auction_id')
        auction = get_object_or_404(AuctionItem, pk=auction_id)
        auction.delete()
        return redirect('artist_uploaded_auction') 
    return HttpResponseBadRequest("Invalid request method")

from django.shortcuts import render, redirect
from .models import User_Bid, AuctionListing

# def approve_bid(request, art_id):
#     try:
#         bid = User_Bid.objects.get(auction_item__id=art_id)
        
#         # Print debug information
#         print(f"Found bid: {bid}")
        
#         # Create an instance of AuctionListing and update its fields
#         auction_listing = AuctionListing.objects.create(
#             auction_item=bid.auction_item,
#             buyer=bid.buyer,
#             seller=bid.seller,
#             latest_price=bid.bid_price,
#             end_date=bid.auction_item.end_date,
#         )
        
#         # Additional logic (if needed) before saving to the database
#         auction_listing.save()
        
#         # Redirect or render a response as needed
#         return redirect('artist_uploaded_auction')
#     except User_Bid.DoesNotExist:
#         # Handle the case where the bid does not exist
#         print(f"Bid with art_id {art_id} does not exist.")
#         return render(request, 'bid_not_found.html')  # Create a template for displaying a custom error message
    

from django.shortcuts import render
from .models import AuctionListing

def notification(request):
    final_winners = AuctionListing.objects.filter(buyer=request.user)
    print(final_winners)
    return render(request, 'notification.html', {'final_winners': final_winners})


from django.shortcuts import get_object_or_404

def notification_view(request, art_id):
    notification = get_object_or_404(AuctionListing, auction_item_id=art_id)
    return render(request, 'notification_view.html', {'notification': notification})


def auction_orderdetails(request,id):
    price = AuctionListing.objects.get(id=id)
    user=request.user.id
    buyer=User.objects.get(id=user)
    
    if request.method == "POST":
        number = request.POST.get("Phone")
        email = request.POST.get("email")
        locality = request.POST.get("locality")
        state = request.POST.get("State")
        pincode = request.POST.get("pin")
        city = request.POST.get("City")
        landmark = request.POST.get("landmark")
        address = request.POST.get("address")

        details=AuctionOrder(
            user = buyer,
            auctionlisting=price,
            buyer_email = email,
            buyer_phone = number,
            buyer_pincode = pincode,
            buyer_state = state,
            buyer_city = city,
            buyer_address = address,
            buyer_locality = locality,
            buyer_landmark = landmark
        )

        details.save()
        return redirect('AuctionPayment',id=details.id)
        

    return render(request,'auction_orderdetails.html',{"price":price})

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def AuctionPayment(request,id):
    price = AuctionListing.objects.get(id=id)
    print(price.latest_price)
    currency = 'INR'
    amount = int(price.latest_price*100)  # Assuming latest_price is a Decimal object
    print(amount)
	# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))
    
	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'AuctionPayment.html', context=context,)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()




def admin_auction(request):
    admin_auction = AuctionItem.objects.all()
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    return render(request,'admin_auction.html',{'admin_auction':admin_auction,'current_date':current_date_ist})

def admin_auction_details(request,id):
    details = AuctionListing.objects.filter(auction_item_id=id)
    return render(request,'admin_auction_details.html',{'details':details})

from django.shortcuts import render, redirect
from .models import AuctionRejectAdmin, AuctionListing

def admin_rejection(request):

    if request.method == "POST":
        art_id = request.POST.get("art_id")
        reason = request.POST.get("rejection_reason")

        auction_art = AuctionItem.objects.get(id=art_id)
        Auction_seller_id = auction_art.user_id

        auction_art.status =False
        auction_art.save()
        
        seller = User.objects.get(id = Auction_seller_id)
        
        rejection = AuctionRejectAdmin(
            art_id=auction_art,
            seller=seller,
            reason=reason,
        )

        rejection.save()

        return redirect('admin_auction')

    return render(request, 'admin_auction.html')

def invoice(request):
    return render(request,'invoice.html')




#Delivary Agent


def delivary_agent_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        pin = request.POST['pin']
        longitude = request.POST['longitude']
        latitude = request.POST['latitude']
        district = request.POST['district']
        state = request.POST['state']
        landmark = request.POST['landmark']
        max_delivery_distance = request.POST['max_delivery_distance']
        address = request.POST['address']
       
        try:

            delivary_registration = DeliveryRegistration(
                name=name,
                email=email,
                phone = phone,
                pin=pin,
                longitude=longitude,
                latitude=latitude,
                district=district,
                state=state,
                landmark=landmark,
                max_delivery_distance=max_delivery_distance,
                address=address
            )
            delivary_registration.save()
            
            email_subject = 'Application recieved  Successfully'
            email_body = f'Thank you for expressing your intrest in working with  ArtVendor as a delivery agent.\n\n'
            email_body += f'We will send updates on your application soon. Please wait for the next steps.'

            send_mail(
                email_subject,
                email_body,
                email,  # Use the provided email address as the sender
                [email],
                fail_silently=False,
            )
            return redirect('login')
        except Exception as e:
            return JsonResponse({'error_message': str(e)}, status=400)
    return render(request, 'delivary_agent_registration.html')


def admin_delivary_view(request):
    delivary_agent=DeliveryRegistration.objects.all()
    return render (request,"admin_delivary_view.html",{"delivary":delivary_agent})

import string
import secrets
def generate_random_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

from django.contrib.auth.hashers import make_password

def admin_delivary_registration(request,delivary_id):
    delivary = DeliveryRegistration.objects.filter(id=delivary_id)

    if request.method == 'POST':
       username=request.POST['name']
       email=request.POST['email'] 
       password=generate_random_password() 
       phone=request.POST['phone']
       

       print(password)

       hashed_password = make_password(password)  

       delivary_registration = User(   
           username=username,
           email=email,
           password=hashed_password
       )
       delivary_registration.save()

       delivary_userdata=UserData(
           user=delivary_registration,
            number=phone,
            role="Delivary"
        )
       delivary_userdata.save()

       status=DeliveryRegistration.objects.get(id=delivary_id)
       status.approval_status="Approved"
       status.user=delivary_registration
       status.save()

       email_subject = 'Your Account Has Been Approved By Admin'
       email_body = f'Username:{username}.\n\n'
       email_body += f'Password:{password}.\n\n'

       send_mail(
                email_subject,
                email_body,
                email,  # Use the provided email address as the sender
                [email],
                fail_silently=False,
            )

    return render(request,"admin_delivary_registration.html",{"delivary":delivary})

def admin_delivary_approval(request): 
    delivary_agent=DeliveryRegistration.objects.all()
    return render(request,"admin_delivary_approval.html",{"delivary_agent":delivary_agent})

def admin_delivary_details(request,id): 
    delivary_details=DeliveryRegistration.objects.get(id=id)
    product_buyer_details=ProductDetails.objects.filter(user=delivary_details.user)
    return render(request,"admin_delivary_details.html",{"delivary_details":delivary_details,"product_buyer_details":product_buyer_details})

def admin_delivary_rejection(request,reject_id): 
    try:
        if request.method == "POST":
            reason = request.POST.get("rejection_details")
            admin_delivary_rejection=DeliveryRegistration.objects.get(id=reject_id)
            email= admin_delivary_rejection.email
            admin_delivary_rejection.approval_status="Rejected"
            admin_delivary_rejection.save() 

            email_subject = 'Rejected By Admin'
            email_body = f'Your are rejected by admin because {reason}\n\n'
            email_body += f'contact admin for furthur clarification: artvendor8@gmail.com'

            send_mail(
                email_subject,
                email_body,
                email,  
                [email],
                fail_silently=False,
            )
            return redirect('admin_delivary_approval')
    except:
        return render(request,"admin_delivary_details.html")

def admin_delivary_approve(request,approve_id): 
    admin_delivary_rejection=DeliveryRegistration.objects.get(id=approve_id)
    email=admin_delivary_rejection.email
    print(email)
    admin_delivary_rejection.approval_status="Approved"
    admin_delivary_rejection.save() 

    email_subject = 'Your Account Has Been Approved By Admin'
    email_body = f'We are pleased to inform you that your account has been approved.\n\n'
    email_body += f'Thank you for your patience and understanding.'

    send_mail(
        email_subject,
        email_body,
        email,  
        [email],
        fail_silently=False,
    )
    return redirect('admin_delivary_approval')

def delivary_profile(request):
    profile_user = User.objects.filter(id=request.user.id)
    profile_userdata = UserData.objects.filter(user=request.user.id)
    profile_delivary = DeliveryProfile.objects.filter(user=request.user.id).exists()

    if profile_delivary:
        profile_delivary = DeliveryProfile.objects.filter(user=request.user.id)

    else:
        profile_delivary = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        userdata1 = UserData.objects.get(user_id=request.user.id)
        userdata1.number = phone
        userdata1.save()

        if profile_delivary:
            profile = DeliveryProfile.objects.get(user_id=request.user.id)
            profile.pin = request.POST.get('pin')
            profile.address = request.POST.get('address')
            profile.latitude = request.POST.get('latitude')
            profile.longitude = request.POST.get('longitude')
            profile.state = request.POST.get('state')
            profile.district = request.POST.get('district')
            profile.max_delivery_km = request.POST.get('max-delivery-km')
            profile.save()
            return redirect('delivary_profile')

        else:
            profile_save = DeliveryProfile(
                pin=request.POST.get('pin'),
                address=request.POST.get('address'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                state=request.POST.get('state'),
                district=request.POST.get('district'),
                max_delivery_km=request.POST.get('max-delivery-km'),
                user_id=request.user.id,
                approval_status="Pending"
            )
            profile_save.save()
            return redirect('delivary_profile')

    return render(request,"delivary_profile.html",{"profile":profile_user,"profile_userdata":profile_userdata,"profile_delivary":profile_delivary})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delivary_dashboard(request):
    assign_count=AuctionOrder.objects.filter(approval_status = "pending").count()
    assign_count=AuctionOrder.objects.filter(approval_status = "approved").count()
    return render(request,'delivary_dashboard.html',{"assign_count":assign_count})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delivary_product_view(request):
    orders = AuctionOrder.objects.filter(approval_status="pending")
    return render(request, 'delivary_product_view.html', {"orders": orders})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delivary_product_approval(request,id):
    order=AuctionOrder.objects.get(id=id)
    order.approval_status = "approved"
    order.save()
    details = ProductDetails(
        auction_order=order,
        user=request.user
    )
    details.save()
    return redirect('accepted_product')
    return render(request,'delivary_product_view.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accepted_product(request):
    product_details=ProductDetails.objects.filter(user=request.user)
    return render(request,'accepted_product.html',{"product_details":product_details})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accepted_product_detail(request,product_detail_id):
    product_details=ProductDetails.objects.get(id=product_detail_id)
    return render(request,'accepted_product_detail.html',{"product_details":product_details})

import random
def generate_otp(request):
    otp_value = str(random.randint(100000, 999999))
    return otp_value

def otp_update(request, otp_id):
    
    product_details = ProductDetails.objects.get(id=otp_id)
    original_request = request.GET.get('request', None)
    random_otp=generate_otp(original_request)
    email=product_details.user.email
    print(email)
    product_details.otp_value = random_otp
    
    product_details.save()

    email_subject = 'OTP Verification'
    email_body = f'Your OTP is:{random_otp}.\n\n'
    email_body += f'We will send updates on your application soon. Please wait for the next steps.'

    send_mail(
                email_subject,
                email_body,
                email,  
                [email],
                fail_silently=False,
            )
    return HttpResponse(status=204)


from django.contrib import messages
def otp_verification(request,otp_verification_id):
    if request.method=="POST":
        entered_value = request.POST.get("otp_value")
        product_details = ProductDetails.objects.get(id=otp_verification_id)
        if product_details.otp_value == entered_value:
            product_details.otp_status="sucess"
            
            product_details.save()
            return redirect('accepted_product_detail',product_detail_id=product_details.id)
        else:
            messages.error(request, "OTP doesn't match")
            return HttpResponse(status=204)
    

from django.utils import timezone
@login_required   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def delivery_update(request,id):
    current_utc_date = timezone.now()
    current_date_ist = current_utc_date + timezone.timedelta(hours=5, minutes=30)
    product_details=ProductDetails.objects.get(id=id)
    product_details.status="delivered"
    product_details.date=current_date_ist
    product_details.save()
    return redirect('accepted_product')
    

def delivary_profile2(request):
    profile_user = User.objects.filter(id=request.user.id)
    profile_userdata = UserData.objects.filter(user=request.user.id)
    profile_delivary = DeliveryProfile.objects.filter(user=request.user.id).exists()

    if profile_delivary:
        profile_delivary = DeliveryProfile.objects.filter(user=request.user.id)

    else:
        profile_delivary = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        userdata1 = UserData.objects.get(user_id=request.user.id)
        userdata1.number = phone
        userdata1.save()

        if profile_delivary:
            profile = DeliveryProfile.objects.get(user_id=request.user.id)
            profile.pin = request.POST.get('pin')
            profile.address = request.POST.get('address')
            profile.latitude = request.POST.get('latitude')
            profile.longitude = request.POST.get('longitude')
            profile.state = request.POST.get('state')
            profile.district = request.POST.get('district')
            profile.max_delivery_km = request.POST.get('max-delivery-km')
            profile.save()
            return redirect('delivary_profile2')

        else:
            profile_save = DeliveryProfile(
                pin=request.POST.get('pin'),
                address=request.POST.get('address'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                state=request.POST.get('state'),
                district=request.POST.get('district'),
                max_delivery_km=request.POST.get('max-delivery-km'),
                user_id=request.user.id,
                approval_status="Pending"
            )
            profile_save.save()
            return redirect('delivary_profile2')

    return render(request,"delivary_profile2.html",{"profile":profile_user,"profile_userdata":profile_userdata,"profile_delivary":profile_delivary})

def delivary_password_update(request):
    if request.method=='POST':
        user=User.objects.get(username=request.user.username)
        password=request.POST.get('password')
        hashed_password = make_password(password)
        user.password=hashed_password
        user.save()
        return redirect('delivary_password_update')
    return render(request,'delivary_password_update.html')

def products(request): 
    return render(request,"products.html")