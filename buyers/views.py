from django.shortcuts import render

# Create your views here.
# def home(request):
#     return render(request, "buyers/home_page.html")

def contact_page(request):
    return render(request, "buyers/contact_page.html", {})
