from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def payment_process(request):
    transactionID = 1

    paypal_dict = {                        # duration unit ("M for Month")
        'business': 'nikhil.thakur929@gmail.com',
        'amount': '10.00',
        'item_name': 'Subscription',
        'invoice': "inv4", # it should be unique
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payment:done')),
        'cancel_return': request.build_absolute_uri(reverse('payment:cancelled'))
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'form': form})

#'notify_url': request.build_absolute_uri(reverse('paypal')),

@csrf_exempt
def payment_done(request):
    print(request)
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'payment/done.html', context)

@csrf_exempt
def payment_cancelled(request):
    args = {'post': request.POST, 'get': request.GET}
    return render(request, 'payment/done.html', args)
