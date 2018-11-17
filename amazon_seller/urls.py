from django.conf.urls import url
from .views import addAmazonAccount, setupSellerAccount, home
from orders.views import OrdersListView

urlpatterns = [
    url(r'^setup/$', setupSellerAccount, name='setup'),
    url(r'^add/$', addAmazonAccount, name='add'),
    url(r'^home/$', home, name='home'),
    url(r'^orders/$', OrdersListView.as_view(), name='orders'),
]
