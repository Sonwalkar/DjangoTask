from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db import IntegrityError
from .models import User
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
  

#send teacher's and student's information to index page.
def index(request):
    return render(request, "credents/index.html",{
        "teachers": User.objects.filter(is_teacher=True),
        "students": User.objects.filter(is_student=True)
    })
   

#log in user
def login_view(request):
    #check method as post
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'credents/login.html', {
                "msg":"Invalid Username or Password"
            })
    else:
        return render(request, "credents/login.html")

#log out user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#register user
def register(request):
    #if user is not authenticated or is_student not give access
    if not request.user.is_authenticated or request.user.is_student:
        return HttpResponse("You are not authorized")
    
    #if user is authenticated add/register user in database
    if request.user.is_authenticated and request.method == "POST":
        acctype = request.POST.get("acc_type")
        username = request.POST.get("username")
        email= request.POST.get("email")
        password = request.POST.get("password")
        repassword = request.POST.get("re_password")

        if password != repassword:
            return render(request, "credents/register.html", {
                "pwd_not_match": "Passwords must match."
            })
        try:
            #add user if user is super admin
            if acctype == "super_admin":
                user = User.objects.create_user(username, email, password, is_super_admin=True)
                user.save()
                group = Group.objects.get(name='super_admin')
                user.groups.add(group)

            #add user if user is teacher
            elif acctype == "teacher":
                user = User.objects.create_user(username, email, password, is_teacher=True)
                user.save()
                group = Group.objects.get(name='teacher')
                user.groups.add(group)

            #add user if user is student
            else:
                user = User.objects.create_user(username, email, password, is_student=True)
                user.save()
                group = Group.objects.get(name='students')
                user.groups.add(group)
        
        #if user is already exist show error
        except IntegrityError:
            return render(request, "credents/register.html",{
                "msg":"Username already exist!"
            })
        
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "credents/register.html")
