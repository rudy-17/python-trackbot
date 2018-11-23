from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .models import Transactions
from django.contrib.auth import get_user_model

# Create your views here.

@csrf_exempt
def payment_done(request, *args):
    if request.POST:
        User = get_user_model()
        user = User.objects.filter(email = request.POST.get("custom"))[0]
        if user.is_authenticated and not user.is_superuser:
            if request.POST:
                amount = request.POST.get('payment_gross')
                if amount == '14.99':
                    type = 'Professional'
                elif amount == '9.99':
                    type = 'Starter'
                else:
                    type = 'Business'
                print(type)
                obj = Transactions.objects.get_or_create(
                    user = user,
                    transactionID = request.POST.get('txn_id'),
                    transactionType = type,
                    amount = amount,
                    active = True
                )
                print(obj)
    return redirect('/buyers/subscription')

@csrf_exempt
def payment_cancelled(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'payment/done.html', args)

# @csrf_exempt
# def payment_process(request):
#     transactionID = 1
#
#     paypal_dict = {
#         'business': 'nikhil.thakur929@gmail.com',
#         'amount': '10.00',
#         'item_name': 'Subscription',
#         'invoice': "inv4", # it should be unique
#         'currency_code': 'USD',
#         'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
#         'return_url': request.build_absolute_uri(reverse('payment:done')),
#         'cancel_return': request.build_absolute_uri(reverse('payment:cancelled')),
#         'user': request.user,
#         'rm': 2
#     }
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     return render(request, 'payment/process.html', {'form': form})
