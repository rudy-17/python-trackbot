from django.shortcuts import render
from django.views.generic import ListView
from collections import defaultdict
from .models import Orders
from tracking.models import TrackingDetails

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

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersListView, self).get_context_data(*args, **kwargs)
        context['my_context'] = get_context_with_modal(context['object_list'])
        # for each in context['object_list']:
        #     order = Orders.objects.filter(orderNumber=each.orderNumber)
        #     trackingID = order[0].trackingid_set.all()
        #     order = order.values()[0]
        #     if len(trackingID) > 0:
        #         temp = {}
        #         temp['TrackingNumber'] = trackingID[0].trackingID
        #         dates = TrackingDetails.objects.filter(trackingID=trackingID[0]).values('date').distinct()
        #         for h in dates:
        #             temp[h['date']] = TrackingDetails.objects.filter(date=h['date'], trackingID=trackingID[0]).values('time', 'activity')
        #         order['track'] = temp
        #     context['my_context'].append(order)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        user_seller = request.user.selleraccount_set.all()
        if len(user_seller) > 0:
            user_seller = user_seller[0]
        else:
            user_seller = None
        query   = request.GET.get('q', None)
        if query is not None:
            return Orders.objects.search(query, self.request.user)
        return Orders.objects.filter(user_seller=user_seller)

class OrdersSearchView(ListView):
    template_name = 'buyers/home_page.html'
    get_context_with_modal = get_context_with_modal

    def get_context_data(self, *args, **kwargs):
        context = super(OrdersSearchView, self).get_context_data(*args, **kwargs)
        context['my_context'] = get_context_with_modal(context['object_list'])
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query   = request.GET.get('q', None)
        if query is not None:
            return Orders.objects.searchExact(query)
        return None
