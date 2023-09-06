from telnetlib import AUTHENTICATION
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserData
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout as django_logout


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
    


def login_view(request):
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


def Artist_view(request):
    return render(request,"Artist_view.html")
    
        
   

def logout_view(request):
    logout(request)
    return redirect('login')


# def register_user(request):
#     form = UserRegistrationForm()
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             # Process form data and create user
#             name = form.cleaned_data['username']
#             email = form.cleaned_data['useremail']
#             mobile_number = form.cleaned_data['usernumber']
#             role = form.cleaned_data['userrole']
#             password = form.cleaned_data['userpassword']
            
#             user = User.objects.create_user(
#                 username=email,
#                 email=email,
#                 password=password,
#                 first_name=name
#             )
#             user = authenticate(username=email, password=password)
#             if user is not None:
#                 lg(request, user)
#                 return redirect('login')  # Redirect to a success pageS               
#             # Redirect to success page or perform other actions
#             else:
#                 messages.info(request,"email already exists")
#         else:
#             name = form.cleaned_data['username']
#             email = form.cleaned_data['useremail']
#             mobile_number = form.cleaned_data['usernumber']
#             role = form.cleaned_data['userrole']
#             password = form.cleaned_data['userpassword']
#             print(name,email,mobile_number,role,password)
#             form = UserRegistrationForm()
    
#     return render(request, 'signup.html', {'form': form})


# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('Artist_view')  # Redirect to a success page
#             else:
#                 form.add_error('email', "Invalid credentials. Please try again.")  # Add error to the email field
#     else:
#         form = UserLoginForm()

#     return render(request, 'login.html', {'form': form})

