from payment.models import Transactions
from django.utils import timezone

def checkSubscription(request):
    user = request.user
    qs = Transactions.objects.filter(user=request.user, active=True)
    if len(qs) > 0:
        transaction = qs[0]
        z = timezone.now() - transaction.dateTime
        # 1day = 86400seconds
        duration = transaction.duration
        if z.days > duration:
            transaction.active = False
            transaction.save()
            request.session['subscribed'] = False
            return {'status': False}
        else:
            request.session['subscribed'] = True
            return {'status': True, 'days-left': duration - z.days, 'transaction': transaction, 'duration': duration}
    else:
        request.session['subscribed'] = False
        return {'status': False}
