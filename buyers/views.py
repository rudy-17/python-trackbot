from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from payment.models import Transactions
from django.utils import timezone
from payment.utils import checkSubscription

def contact_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return render(request, "buyers/contact_page.html", {})
    else:
        return redirect('/accounts/login')

def subscription_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        context = {}
        form = []
        amount = ['9.99', '14.99', '19.99']
        result = checkSubscription(request)
        if result.get('status'):
            obj = result.get('transaction')
            for i in range(3):
                if obj.amount == amount[i]:
                    form.append({'sandbox': "active", 'daysLeft': result.get('days-left'), 'daysPercent': (30 - result.get('days-left'))/30*100 })
                else:
                    form.append({'sandbox': ''})
            request.session['subscribed'] = True
        else:
            for i in range(3):
                paypal_dict = {
                    'business': 'nikhil.thakur929@gmail.com',
                    'amount': amount[i],
                    'item_name': 'Subscription',
                    'invoice': "inv4", # it should be unique
                    'currency_code': 'USD',
                    'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
                    'return_url': request.build_absolute_uri(reverse('payment:done')),
                    'cancel_return': request.build_absolute_uri(reverse('payment:cancelled')),
                    'rm': 2,
                    'custom': request.user.email
                }
                form.append(PayPalPaymentsForm(initial=paypal_dict))
            request.session['subscribed'] = False
        context['form1'] = form[0]
        context['form2'] = form[1]
        context['form3'] = form[2]
        return render(request, "buyers/subscription.html", context)
    else:
        return redirect('/accounts/login')
