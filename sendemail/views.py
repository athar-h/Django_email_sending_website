from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import All_users
from django.http import JsonResponse
import ast
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            user_exist = authenticate(username=username,password=password)
            if user_exist:
                login(request,user_exist)
                if request.GET.get('next',None):
                    return redirect(request.GET['next'])
    # login function saves user info in to the session
                return redirect("home/")
            else:
                messages.error(request,"invalid password")

        else:
            messages.error(request,"user does not exist")
            return redirect("register")
    return render(request,'login.html')

def register_page(request):
    message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if User.objects.filter(username=username).exists():
            message = "username not available"
            print("username not available")
            return redirect("register",{"data":message})
        else:
            user_obj = User.objects.create(
                username=username,
                email = email,
                )
            user_obj.set_password(password)
            user_obj.save()
            return redirect("home")
    return render(request,"register.html")

@login_required(login_url="/login/")
def home_page(request):
    user_name = request.user.get_username().upper()
    return render(request,"base.html",{"username":user_name})

@login_required(login_url="/login/")
def api_view(request):
    if request.method == "POST":
        subs = str(request.POST.get("subs")).capitalize()
        subs = ast.literal_eval(subs)
    # javascript true to Python True
        print(subs)
        user_name = request.user.get_username()
        print(user_name)
        email = request.user.email
        print(email)
        if subs:
            send_mail(
                "Congratulations On subscription",
                "Thank you for showing interest.we appreciate your efforts",
                "atharbusines@gmail.com",
                [email],
                fail_silently=False,
        )

        if All_users.objects.filter(username=user_name).exists():
            user_obj = All_users.objects.get(username=user_name)
            user_obj.subs_detail = subs
            user_obj.save()
        else:
            usr = All_users(username=user_name, email_address=email, subs_detail=subs)
            usr.save()
        resp = {
            "status":"success"
        }
        
    return JsonResponse(resp)
    

def logout_page(request):
    logout(request)
    messages.success(request,"you logged out successfully")
    return redirect("/login/")
