from django.shortcuts import render, redirect, reverse
from .models import SellerAccount, EbayAccount
from django.http import HttpResponse
from .forms import AmazonLoginForm
from .models import SellerAccount
from django.contrib.auth import get_user_model
from paypal.standard.forms import PayPalPaymentsForm
from payment.models import Transactions
from django.utils import timezone
from payment.utils import checkSubscription
from payment.models import Transactions
from datetime import timedelta
from collections import defaultdict
from django.core.mail import send_mail

def upgrade(request):
    pass

def help_page(request):
    if request.user.is_authenticated:
        if request.POST:
            tba = request.POST.get('tba_no')
            #message = 'Following tracking number of '+request.user.email+' is missing: '+tba
            # send_mail(
            #     'Re. Tracking Number',
            #     message,
            #     'wjeff.fortin@yahoo.com',
            #     ['info@beezytrack.com'],
            #     fail_silently=False,
            #     auth_user='wjeff.fortin@yahoo.com',
            #     auth_password='Beezytrack'
            # )
        return render(request, 'seller/help.html', {})
    return redirect('/accounts/login')

def remove(request):
    if request.user.is_authenticated:
        account = SellerAccount.objects.filter(user=request.user)
        if account:
            account.delete()
            return redirect('/amazon/setup')
    return redirect('/amazon/setup')

def profile(request):
    if request.user.is_authenticated:
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
    if request.user.is_authenticated and request.is_ajax:
        user = request.user
        for key, values in request.POST.items():
            setattr(user, key, values)
            user.save()
        return HttpResponse('Done')
    else:
        return redirect('/accounts/login')

def setupSellerAccount(request):
    if request.user.is_authenticated:
        if request.session.get('subscribed'):
            form = AmazonLoginForm(request.POST or None)
        else:
            form = False
        context = {}
        account = SellerAccount.objects.filter(user=request.user)
        create = True
        if account:
            create = False
            context['email'] = account[0].email
        if request.POST and request.session.get('subscribed'):
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
        inst = EbayAccount.objects.filter(user = request.user)
        if inst:
            context['ebayActive'] = True
        return render(request, 'seller/addThirdPartyAccounts.html', context)
    else:
        return redirect('/accounts/login')

def setupEbayAccount(request):
    if request.user.is_authenticated:
        context = {}
        if request.POST:
            obj = EbayAccount(
                user = request.user,
                activate = True
            )
            obj.save()
            context['notify'] = True
        if request.session.get('subscribed'):
            form = AmazonLoginForm(request.POST or None)
        else:
            form = False
        account = SellerAccount.objects.filter(user=request.user)
        create = True
        if account:
            create = False
            context['email'] = account[0].email
        context['form'] = form
        context['create'] = create
        inst = EbayAccount.objects.filter(user = request.user)
        if inst:
            context['ebayActive'] = True
        return render(request, 'seller/addThirdPartyAccounts.html', context)
    else:
        return redirect('/accounts/login')

def home(request):
    if request.user.is_authenticated:
        context = {}
        qs = Transactions.objects.filter(user = request.user)
        context['object_list'] = qs
        return render(request, 'seller/home.html', context)
    else:
        return redirect('/accounts/login')

def subscription_page(request):
    if request.user.is_authenticated:
        form = {}
        plans = {
            'Beezytrack': {
                'mo': 4.99,
                'yr': 49.99
            },
            'Pro Drop Shipper': {
                'mo': 4.99,
                'yr': 49.99
            },
            'Combo (Beezytrack + Pro Drop Shipper)': {
                'mo': 9.98,
                'yr': 99.98
            }
        }
        result = checkSubscription(request)
        if result.get('status'):
            obj = result.get('transaction')
            duration_int = result.get('duration')
            flag=0
            if duration_int == 30:
                duration_str = 'mo'
            elif duration_int == 365:
                duration_str = 'yr'
            for planName, attrs in plans.items():
                temp = {}
                for duration, amount in attrs.items():
                    if obj.plan == planName and duration_str == duration:
                        temp[duration] = {'status': True, 'amount': {'value': amount}, 'sandbox': "active", 'daysLeft': result.get('days-left'), 'daysPercent': (duration_int - result.get('days-left'))/duration_int*100 }
                        flag=1
                    else:
                        temp[duration] = {'status': False, 'sandbox': '', 'amount': {'value': amount}}
                if flag:
                    temp['active'] = duration_int
                    flag = 0
                form[planName] = temp
        else:
            for planName, attrs in plans.items():
                temp = {}
                for duration, amount in attrs.items():
                    paypal_dict = {
                        'business': 'nikhil.thakur929@gmail.com',
                        'amount': amount,
                        'item_name': planName,
                        'invoice': duration, # it should be unique
                        'currency_code': 'USD',
                        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
                        'return_url': request.build_absolute_uri(reverse('payment:done')),
                        'cancel_return': request.build_absolute_uri(reverse('payment:cancelled')),
                        'rm': 2,
                        'custom': request.user.email
                    }
                    temp[duration] = (PayPalPaymentsForm(initial=paypal_dict))
                form[planName] = temp
        return render(request, "seller/subscription.html", {'form': form})
    else:
        return redirect('/accounts/login')

def cancelSubscription(request):
    if request.user.is_authenticated and request.session.get('subscribed') == True:
        user = request.user
        qs = Transactions.objects.filter(user=user, active=True)[0]
        setattr(qs, 'active', False)
        qs.save()
        return redirect('/amazon/subscription')
    else:
        return redirect('/accounts/login')
