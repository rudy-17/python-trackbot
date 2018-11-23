from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model

def home_page(request):
    user = request.user
    print("hello")
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/amazon/home')
        else:
            return redirect('/buyers/home')
    else:
        return render(request, 'buyers/homepage.html', {})
