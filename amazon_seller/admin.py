from django.contrib import admin
from .models import SellerAccount, EbayAccount


# Register your models here.
admin.site.register(SellerAccount)
admin.site.register(EbayAccount)
