from django.shortcuts import render, redirect
from .models import SellerAccount
from django.http import HttpResponse
from .forms import AmazonLoginForm
from .models import SellerAccount
from django.contrib.auth import get_user_model

# Create your views here.
def addAmazonAccount(request):
    return HttpResponse("Done")

def remove(request):
    if request.user.is_authenticated and request.user.is_superuser:
        account = SellerAccount.objects.filter(user=request.user)
        if account:
            account.delete()
            return redirect('/amazon/setup')
    return redirect('/amazon/setup')

def profile(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        user = request.user
        context['Username'] = { 'label': user.username, 'code': 'username' }
        context['Email'] = {'label': user.email, 'code': 'email' }
        context['First Name'] = { 'label': user.first_name, 'code': 'first_name' }
        context['Last Name'] = { 'label': user.last_name, 'code': 'last_name' }
        return render(request, 'seller/profile.html', {'obj_list' : context})
    else:
        return redirect('/accounts/login')

def updateuser(request):
    if request.user.is_authenticated and request.user.is_superuser and request.is_ajax:
        user = request.user
        for key, values in request.POST.items():
            setattr(user, key, values)
            user.save()
        return HttpResponse('Done')
    else:
        return redirect('/accounts/login')

def setupSellerAccount(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        form = AmazonLoginForm(request.POST or None)
        account = SellerAccount.objects.filter(user=request.user)
        create = True
        if account:
            create = False
            context['email'] = account[0].email
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
                return redirect('/amazon/setup')
        context['form'] = form
        context['create'] = create
        return render(request, 'seller/addThirdPartyAccounts.html', context)
    else:
        return redirect('/accounts/login')

def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'seller/home.html', {})
    else:
        return redirect('/accounts/login')
