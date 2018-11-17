from django.shortcuts import render, redirect
from .models import SellerAccount
from django.http import HttpResponse
from .forms import AmazonLoginForm
from .models import SellerAccount

# Create your views here.
def addAmazonAccount(request):
    return HttpResponse("Done")

def setupSellerAccount(request):
    if request.user.is_authenticated and request.user.is_superuser:
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
    else:
        return redirect('/accounts/login')

def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'seller/home.html', {})
    else:
        return redirect('/accounts/login')
