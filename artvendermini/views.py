from telnetlib import AUTHENTICATION
from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import UserData
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

@login_required
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
    return render(request, "Artist_view.html", {'artdata': artdata,'total':total_arts_uploaded,'art':arts_approved})

@login_required
def index(request):
    artdata = UploadArtDetail.objects.filter(approval_status='approved')
    return render(request, "index.html", {'artdata': artdata})


def admin_pannel(request):
    if request.method == 'POST':
        art_id = request.POST.get('art_id')
        approval_status = request.POST.get('approval_status')

        try:
            art = UploadArtDetail.objects.get(id=art_id)
            art.approval_status = approval_status
            art.is_approved = (approval_status == 'approved')  # Set is_approved based on approval_status
            art.save()
            return redirect('admin_pannel')
        except UploadArtDetail.DoesNotExist:
            return HttpResponse("Art not found.")

    # Retrieve all art data for display in the table
    art_data = UploadArtDetail.objects.all()
    return render(request, 'admin_pannel.html', {'art_data': art_data})


from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadArtDetail

def update_art(request, art_id):
    art = get_object_or_404(UploadArtDetail, id=art_id)

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
        return render(request, 'update_art.html', {'art': art, 'is_approved': art.is_approved})
    



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





    





