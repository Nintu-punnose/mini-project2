from telnetlib import AUTHENTICATION
from urllib import request
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import UserData, artOrder
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UploadArtDetail,SellerProfile



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
                else:
                    return redirect('admin_pannel')
            else:
                # Display error message using messages framework
                messages.info(request, "Invalid credentials. Please try again.")
        else:
            # Display error message using messages framework
            messages.info(request, "Please provide both username and password.")

    return render(request, 'login.html')


# def Artist_view(request):
#     return render(request,"Artist_view.html")

from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
@login_required
@never_cache
def logout_view(request):
    auth.logout(request)
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
    return render(request,'seller_profile.html',{'user':user,'userdata':userdata,'seller':seller})



def images(request):
    images=UploadArtDetail.objects.filter(approval_status='approved')
    return render(request,'images.html',{'images':images})

def image_detail(request,id):
    img_id = get_object_or_404(UploadArtDetail, id=id)
    return render(request,'image_detail.html',{'img_id':img_id})

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

# def Artist(request):
#     artistdata1=User.objects.all()
#     # artistdata2=UserData.objects.filter(role='Artist')
#     artistdata3=SellerProfile.objects.all()
#     # context={'artistdata1':artistdata1,'artistdata2':artistdata2,'artistdata3':artistdata3 }
#     data=UserData.objects.filter(role='Artist')
#     l=[]
#     for i in data:
#         l+=SellerProfile.objects.filter(user=i.user)
    
#     return render(request,'Artist.html',{'artist':l})

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





# from django.shortcuts import render
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseBadRequest


# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
# 	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def payment(request):
# 	currency = 'INR'
# 	amount = 20000 # Rs. 200

# 	# Create a Razorpay Order
# 	razorpay_order = razorpay_client.order.create(dict(amount=amount,
# 													currency=currency,
# 													payment_capture='0'))

# 	# order id of newly created order.
# 	razorpay_order_id = razorpay_order['id']
# 	callback_url = 'paymenthandler/'

# 	# we need to pass these details to frontend.
# 	context = {}
# 	context['razorpay_order_id'] = razorpay_order_id
# 	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
# 	context['razorpay_amount'] = amount
# 	context['currency'] = currency
# 	context['callback_url'] = callback_url

# 	return render(request, 'payment.html', context=context)


# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):

# 	# only accept POST request.
# 	if request.method == "POST":
# 		try:
		
# 			# get the required parameters from post request.
# 			payment_id = request.POST.get('razorpay_payment_id', '')
# 			razorpay_order_id = request.POST.get('razorpay_order_id', '')
# 			signature = request.POST.get('razorpay_signature', '')
# 			params_dict = {
# 				'razorpay_order_id': razorpay_order_id,
# 				'razorpay_payment_id': payment_id,
# 				'razorpay_signature': signature
# 			}

# 			# verify the payment signature.
# 			result = razorpay_client.utility.verify_payment_signature(
# 				params_dict)
# 			if result is not None:
# 				amount = 20000 # Rs. 200
# 				try:

# 					# capture the payemt
# 					razorpay_client.payment.capture(payment_id, amount)

# 					# render success page on successful caputre of payment
# 					return render(request, 'payment.html')
# 				except:

# 					# if there is an error while capturing payment.
# 					return render(request, 'paymentfail.html')
# 			else:

# 				# if signature verification fails.
# 				return render(request, 'paymentfail.html')
# 		except:

# 			# if we don't find the required parameters in POST data
# 			return HttpResponseBadRequest()
# 	else:
# 	# if other than POST request is made.
# 		return HttpResponseBadRequest()
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
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {'orders': orders})












