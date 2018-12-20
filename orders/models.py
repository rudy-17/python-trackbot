from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from amazon_seller.models import SellerAccount

# Create your models here.

class OrderManager(models.Manager):
    def search(self, query, user):
        user_seller = user.selleraccount_set.all()
        if user_seller:
            user_seller = user_seller[0]
            lookups = Q(productName__icontains=query, user_seller=user_seller) | Q(trackingID__icontains=query, user_seller=user_seller)
            return self.get_queryset().filter(lookups).distinct()
        else:
            return None

    def searchExact(self, query):
        lookups = Q(trackingID__iexact=query)
        print(query)
        print(self.get_queryset().filter(trackingID__iexact=query))
        return self.get_queryset().filter(lookups).distinct()

class Orders(models.Model):
    user_seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
    orderData   = models.CharField(max_length=120)
    orderNumber = models.CharField(max_length=120)
    trackingID = models.CharField(max_length=150)
    orderStatus = models.CharField(max_length=120)
    shippingAddress = models.TextField(max_length=120)
    productName = models.CharField(max_length=120)
    productImage = models.TextField()
    objects = OrderManager()

    def __str__(self):
        return self.orderNumber
