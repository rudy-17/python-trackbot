from django.conf.urls import url
from .views import setupSellerAccount, home, profile, updateuser, remove, subscription_page, cancelSubscription, help_page, upgrade, setupEbayAccount
from orders.views import OrdersListView

urlpatterns = [
    url(r'^setup/$', setupSellerAccount, name='setup'),
    url(r'^home/$', home, name='home'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^updateuser/$', updateuser, name='updateuser'),
    url(r'^orders/$', OrdersListView.as_view(), name='orders'),
    url(r'^remove/$', remove, name='remove'),
    url(r'^subscription/$', subscription_page, name='subscription'),
    url(r'^subscription/cancel$', cancelSubscription, name='cancelSubscription'),
    url(r'^help$', help_page, name='help'),
    url(r'^ebay$', setupEbayAccount, name='ebay'),
    #url(r'^upgrade$', upgrade, name='upgrade'),
]
