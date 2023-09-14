from telnetlib import AUTHENTICATION
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserData
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UploadArtDetail



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
                return redirect('Artist_view')  # Redirect to your artist view
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




def edit_art(request):
    return redirect('Artist_view')






    





