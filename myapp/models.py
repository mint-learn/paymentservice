from django.db import models

class Order(models.Model):
    from_account = models.IntegerField(null=True)
    merchant_order_id = models.IntegerField()
    order_time = models.DateTimeField()
    payment_id = models.IntegerField(primary_key=True)
    payment_time = models.DateTimeField(null=True)
    price = models.IntegerField()
    stamp = models.CharField(max_length=255)
    to_account = models.IntegerField()


class Account(models.Model):
    balance = models.IntegerField()
    email = models.EmailField(max_length=255)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class RefundOrder(models.Model):
    refund_id = models.IntegerField(primary_key=True)
    refund_time = models.CharField(max_length=255)
    payment_id = models.IntegerField()
    price = models.IntegerField()
