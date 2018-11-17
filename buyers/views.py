from django.shortcuts import render, redirect

# Create your views here.
# def home(request):
#     return render(request, "buyers/home_page.html")

def contact_page(request):
    if request.user.is_authenticated and not request.user.is_super:
        return render(request, "buyers/contact_page.html", {})
    else:
        return redirect('/accounts/login')
