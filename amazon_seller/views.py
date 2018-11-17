from django.shortcuts import render, redirect
from .models import SellerAccount
from django.http import HttpResponse
from .forms import AmazonLoginForm
from .models import SellerAccount

# Create your views here.
def addAmazonAccount(request):
    return HttpResponse("Done")

def setupSellerAccount(request):
    form = AmazonLoginForm(request.POST or None)
    account = SellerAccount.objects.filter(user=request.user)
    create = True
    if account:
        create = False
    if request.POST:
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            obj = SellerAccount.objects.get_or_create(
                user = request.user,
                email = email,
                password = password
            )
    return render(request, 'seller/addThirdPartyAccounts.html', {'form': form, 'create': create})

def home(request):
    return render(request, 'seller/home.html', {})
