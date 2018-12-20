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
        if user.is_authenticated:
            if request.POST:
                amount = request.POST.get('payment_gross')
                type = request.POST.get('item_name')
                d = request.POST.get('invoice')
                if d == 'mo':
                    duration = 30
                elif d == 'yr':
                    duration = 365
                obj = Transactions.objects.get_or_create(
                    user = user,
                    transactionID = request.POST.get('txn_id'),
                    plan = type,
                    duration = duration,
                    amount = amount,
                    active = True
                )
    return redirect('/amazon/subscription')

@csrf_exempt
def payment_cancelled(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'payment/cancelled.html', args)
