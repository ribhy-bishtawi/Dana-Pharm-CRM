import imp
from django.db import models


class Customer(models.Model):
    email = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    ordersCount = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
