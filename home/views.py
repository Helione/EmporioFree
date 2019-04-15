#https://docs.djangoproject.com/en/2.1/topics/auth/default/#built-in-auth-forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout



def home(request):
    return render(request,'home.html')

def my_logout(request):
    logout(request)
    return redirect('home')

