from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Transactions(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    transactionID = models.CharField(max_length=150)
    transactionType = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    active = models.BooleanField()
    dateTime = models.DateTimeField(auto_now_add=True)
