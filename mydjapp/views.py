from django.http import HttpResponse 
from django.shortcuts import render, redirect
from . import models 
from .models import Register  # your model
import time
import hashlib

def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
            request.session['sunm'] = None
            request.session['srole'] = None
            response = get_response(request)
        else:
            response = get_response(request)
        return response    
    return middleware

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def service(request): 
    return render(request, "service.html")
    
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"output": ""})
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        gender = request.POST.get("gender")
        info = time.asctime()
        
        hashed_pwd = hashlib.sha1(password.encode()).hexdigest().upper()
        hashed_pwd = "*" + hashed_pwd


        # Insert data using model class
        p = models.Register(
            name=name, email=email, password=hashed_pwd, mobile=mobile,
            address=address, city=city, gender=gender, status=0, role="user",
            info=info
        )
        p.save()

        print("User registered successfully.......")
        
        return render(request, "register.html", {"output": "User registered successfully....."})

def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"output": ""})
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

       
        # Hash the password to match stored value
        hashed_pwd = hashlib.sha1(password.encode()).hexdigest().upper()
        hashed_pwd = "*" + hashed_pwd  # emulate MySQL PASSWORD() style used on registration

        # First, check if user exists with these credentials (regardless of status)
        user_details = models.Register.objects.filter(email=email, password=hashed_pwd)

        # Backward compatibility: if no match with hashed password, try legacy plaintext
        if len(user_details) == 0:
            user_details = models.Register.objects.filter(email=email, password=password)
            if len(user_details) == 0:
                return render(request, "login.html", {"output": "Invalid email or password"})

        user = user_details[0]

        # If account is not approved yet, show a clear message
        if user.status != 1 and user.role != "admin":
            return render(request, "login.html", {"output": "Your account is pending admin approval."})

        # Store user details in session
        request.session["sunm"] = user.email
        request.session["srole"] = user.role

        if user.role == "admin":
            return redirect("/myadmin/")
        else:
            return redirect("/user/")
