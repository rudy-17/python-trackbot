from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class SellerAccount(models.Model):
    user     = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email    = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email
