"""trackbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', home_page, name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^amazon/', include(("amazon_seller.urls", "amazon"), namespace='amazon')),
    url(r'^buyers/', include(("buyers.urls", "buyers"), namespace='buyers')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include(('payment.urls', 'payment'), namespace='payment')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
