from django.db import models
from orders.models import Orders
from django.db.models.signals import pre_save, post_save
from .amz import AmzScraper
from django.contrib.auth import get_user_model
from amazon_seller.models import SellerAccount
from orders.models import Orders

class TrackingDetailsManager(models.Manager):
    def create(self, orders, trackingStatus):
        print("Neeche")
        print(trackingStatus)
        if len(trackingStatus) > 0:
            for key, values in trackingStatus.items():
                for each in values:
                    u = TrackingDetails(
                        orders = orders,
                        date = key,
                        time = each[0],
                        activity = each[1],
                    )
                    u.save()


class TrackingDetails(models.Model):
    date = models.CharField(max_length=120)
    time = models.CharField(max_length=120)
    activity = models.TextField()
    orders = models.ForeignKey(Orders, on_delete=models.CASCADE)
    objects = TrackingDetailsManager()


def seller_account_post_save_reciever(sender, instance, *args, **kwargs):
    user = instance.email
    password = instance.password
    data = AmzScraper(year=2018, user = user, password = password, cache_timeout=21600).run()
    print("Done")

    for each in data:
        order_instance = Orders(
            user_seller = instance,
            orderData = each['order-data'],
            orderNumber = each['order-number'],
            orderStatus = each['order-status'],
            shippingAddress = each['shipping-address'],
            paymentMethod = each['payment-method'],
            productName = each['product-name'],
            trackingID = each['trackingID'][12:]
        )
        order_instance.save()
        try:
            tStatus = each.get('tracking-status')
            TrackingDetails.objects.create(order_instance, tStatus)
        except:
            print("No tracking ID")

post_save.connect(seller_account_post_save_reciever, sender=SellerAccount)
