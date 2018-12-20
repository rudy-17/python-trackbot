from django.shortcuts import render, redirect
from django.views.generic import ListView
from collections import defaultdict
from .models import Orders
from tracking.models import TrackingDetails
from payment.utils import checkSubscription

def get_context_with_modal(qs):
    l = []
    if qs:
        for each in qs:
            order = Orders.objects.filter(orderNumber=each.orderNumber)
            u = order[0]
            order = order.values()[0]
            temp = {}
            temp['TrackingNumber'] = u.trackingID
            dates = TrackingDetails.objects.filter(orders=u).values('date').distinct()
            for h in dates:
                temp[h['date']] = TrackingDetails.objects.filter(date=h['date'], orders=u).values('time', 'activity')
            order['track'] = temp
            l.append(order)
    return l

class OrdersListView(ListView):
    template_name = 'orders/orders_list.html'
    get_context_with_modal = get_context_with_modal
    checkSubscription = checkSubscription

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersListView, self).get_context_data(*args, **kwargs)
        context['my_context'] = get_context_with_modal(context['object_list'])
        print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        if request.user.is_authenticated:
            user_seller = request.user.selleraccount_set.all()
            if len(user_seller) > 0:
                user_seller = user_seller[0]
            else:
                user_seller = None
        else:
            user_seller = None
        query   = request.GET.get('q', None)
        if query is not None:
            return Orders.objects.search(query, self.request.user)
        return Orders.objects.filter(user_seller=user_seller)

    def render_to_response(self, context):
        if self.request.user.is_authenticated:
            if self.request.session.get('subscribed') == True:
                return super(OrdersListView, self).render_to_response(context)
            else:
                return redirect('/amazon/subscription')
        return redirect('/accounts/login')

class OrdersSearchView(ListView):
    template_name = 'buyers/dashboard.html'
    get_context_with_modal = get_context_with_modal

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersSearchView, self).get_context_data(*args, **kwargs)
        context['my_context'] = get_context_with_modal(context['object_list'])
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query   = request.GET.get('q', None)
        if query is not None:
            qs = Orders.objects.searchExact(query)
            if len(qs) > 0:
                qs1 = qs[0].user_seller.user.transactions_set.filter(active=True)
                if len(qs1) > 0:
                    return qs
        return None
