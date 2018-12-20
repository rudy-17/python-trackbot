from django.conf.urls import url
from orders.views import OrdersSearchView
from .views import learn_more, contact_page, search_tool_page

urlpatterns = [
    #url(r'^contact/$', contact_page, name='contact'),
    url(r'^home/$', OrdersSearchView.as_view(), name='home'),
    url(r'^learnmore/$', learn_more, name='learn_more'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^searchTool/$', search_tool_page, name='search_tool'),
]
