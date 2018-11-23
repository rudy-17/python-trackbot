from payment.models import Transactions
from django.utils import timezone

def checkSubscription(request):
    user = request.user
    qs = Transactions.objects.filter(user=request.user, active=True)
    if len(qs) > 0:
        transaction = qs[0]
        z = timezone.now() - transaction.dateTime
        # 1day = 86400seconds
        if z.days > 30:
            transaction.active = False
            transaction.save()
            return {'status': False}
        else:
            return {'status': True, 'days-left': 30 - z.days, 'transaction': transaction}
    else:
        return {'status': False}
