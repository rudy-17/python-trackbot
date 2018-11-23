from django.conf.urls import url
from .views import contact_page, subscription_page
from orders.views import OrdersSearchView

urlpatterns = [
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^home/$', OrdersSearchView.as_view(), name='home'),
    url(r'^subscription/$', subscription_page, name='subscription'),
]
