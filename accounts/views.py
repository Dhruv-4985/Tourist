# from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# import random

# # Home View
# def home(request):
#     return render(request, 'index.html')

# User Login
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         pass1 = request.POST.get('pass')
#         user = authenticate(request, username=username, password=pass1)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid username or password!")
#             return redirect('login')

#     return render(request, 'login.html')

# # User Registration with OTP
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 != password2:
#             messages.error(request, "Passwords do not match!")
#             return redirect('signup')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username is already taken!")
#             return redirect('signup')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered!")
#             return redirect('signup')

#         # Generate a 4-digit OTP
#         otp = random.randint(1000, 9999)

#         # Store user details & OTP in session
#         request.session['signup_data'] = {
#             'username': username,
#             'email': email,
#             'password': password1,
#             'otp': otp
#         }

#         # Send OTP via email
#         send_mail(
#             "Your OTP for Signup",
#             f"Your OTP for account verification is {otp}",
#             "tourproject78@gmail.com",  # Use your actual email
#             [email],
#             fail_silently=False,
#         )

#         messages.success(request, "OTP sent to your email. Please verify.")
#         return redirect('verify_otp')

#     return render(request, 'signup.html')

# # OTP Verification View
# def verify_otp(request):
#     if request.method == 'POST':
#         digit1 = request.POST.get("digit1", "")
#         digit2 = request.POST.get("digit2", "")
#         digit3 = request.POST.get("digit3", "")
#         digit4 = request.POST.get("digit4", "")

#         entered_otp = f"{digit1}{digit2}{digit3}{digit4}"

#         signup_data = request.session.get('signup_data', {})

#         if not signup_data:
#             messages.error(request, "Session expired! Please sign up again.")
#             return redirect('signup')

#         if entered_otp == str(signup_data.get('otp')):
#             # Create user account
#             user = User.objects.create_user(
#                 username=signup_data['username'],
#                 email=signup_data['email'],
#                 password=signup_data['password'],
#             )
#             user.save()

#             # Log in the user
#             login(request, user)

#             # Clear session data
#             del request.session['signup_data']

#             messages.success(request, "Account verified successfully!")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid OTP! Please try again.")
#             return redirect('verify_otp')

#     return render(request, 'verify_otp.html')

# # User Logout
# def user_logout(request):
#     logout(request)
#     return redirect('login')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

# Store OTPs temporarily (Ideally, use session or database)
otp_storage = {}

# Home View
def home(request):
    return render(request, 'index.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')

# Register View with OTP Verification
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username is already taken.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email is already registered.")
        if password1 != password2:
            return HttpResponse("Passwords do not match.")
        if len(password1) < 6:
            return HttpResponse("Password must be at least 6 characters long.")

        # Generate OTP
        otp = str(random.randint(1000, 9999))
        otp_storage[email] = otp  # Store OTP temporarily

        # Send OTP via email
        send_mail(
            "Your OTP Code",
            f"Your OTP code is {otp}",
            "your-email@example.com",
            [email],
            fail_silently=False,
        )

        # Store user details in session
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password1

        return redirect('verify_otp')

    return render(request, 'signup.html')

# OTP Verification View
def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('email')
        entered_otp = request.POST.get('otp')

        if email in otp_storage and otp_storage[email] == entered_otp:
            # OTP verified, create the user
            username = request.session.get('username')
            password = request.session.get('password')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Clear stored OTP and session data
            del otp_storage[email]
            del request.session['username']
            del request.session['email']
            del request.session['password']

            return redirect('login')

        else:
            return HttpResponse("Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')
