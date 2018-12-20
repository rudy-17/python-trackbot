from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model

def home_page(request):
    user = request.user
    print("hello")
    if user.is_authenticated:
        return redirect('/amazon/home')
    return redirect('/buyers/home')
