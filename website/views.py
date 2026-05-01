from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
# def login_user(request):
#     if request.method == "POST":
    
#     username_var = request.POST["username"]
#     password_var = request.POST["password"]

#     user = authenticate(username = username_var, password = password_var)

