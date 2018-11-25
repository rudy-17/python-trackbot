from django.conf.urls import url
from .views import addAmazonAccount, setupSellerAccount, home, profile, updateuser, remove
from orders.views import OrdersListView

urlpatterns = [
    url(r'^setup/$', setupSellerAccount, name='setup'),
    url(r'^add/$', addAmazonAccount, name='add'),
    url(r'^home/$', home, name='home'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^updateuser/$', updateuser, name='updateuser'),
    url(r'^orders/$', OrdersListView.as_view(), name='orders'),
    url(r'^remove/$', remove, name='remove'),
]
