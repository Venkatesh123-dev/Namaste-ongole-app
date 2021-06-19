from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from menu.models import Product, Offer
from django.contrib.auth.models import User
from .fields import JSONField
from enum import IntEnum
import math

GST_CHARGES = 5
INTERNET_HANDLING_CHARGES = 2


class OrderTypes(IntEnum):
    NONE = 0
    CASH_ON_DELIVERY = 1
    DELIVERY = 2
    PICK_UP = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PaymentStatus(IntEnum):
    CREATED = 0
    PAID = 1
    REFUND = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class OrderProduct(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product_option = models.ForeignKey(ProductOptions, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    per_price = models.IntegerField(default=0)
    offer = models.ForeignKey(Offer,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)

    def __str__(self):
        if self.offer:
            return f"{self.quantity} of {self.product.product} ({self.offer.title})"
        return f"{self.quantity} of {self.product.product}"

    @property
    def get_json(self):
        return {
            "product": self.product.product,
            "image": self.product.image.url if self.product.image else None,
            "quantity": self.quantity,
            "per_price": self.per_price,
            "total_price": self.total_price,
            "offer": self.offer.title if self.offer else "",
        }

    @property
    def total_price(self):
        return self.quantity * self.per_price

    # def get_total_discount_product_price(self):
    #     return self.quantity * self.product.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_product_price() - self.get_total_discount_product_price()

    # def get_final_price(self):
    #     if self.product.discount_price:
    #         return self.get_total_discount_product_price()
    #     return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    order_placed = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address',
                                         related_name='shipping_address',
                                         on_delete=models.SET_NULL,
                                         blank=True,
                                         null=True)
    coupon = models.ForeignKey('Coupon',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True)
    out_for_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    order_type = models.IntegerField(choices=OrderTypes.choices(),
                                     default=OrderTypes.NONE)
    payment_status = models.IntegerField(choices=PaymentStatus.choices(),
                                         default=PaymentStatus.CREATED)
    delivery_charges = models.IntegerField(default=0, blank=True, null=True)
    gateway_order_id = models.CharField(max_length=100, blank=True, null=True)
    gateway_order_response = JSONField(blank=True, null=True)
    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''
    def __str__(self):
        return self.user.username

    @property
    def products_amount(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.total_price

        if self.coupon:
            total -= self.coupon.amount

        return total

    @property
    def amount_with_delivery(self):
        total = self.products_amount
        if self.order_type == OrderTypes.DELIVERY:
            total += self.delivery_charges

        return math.ceil(total)

    @property
    def amount_with_gst(self):
        total = self.amount_with_delivery
        total += self.gst_amount
        return math.ceil(total)

    @property
    def gst_amount(self):
        total = self.products_amount
        return math.ceil((total * GST_CHARGES) / 100)

    @property
    def internet_charges(self):
        total = self.amount_with_gst
        return math.ceil((total * INTERNET_HANDLING_CHARGES) / 100)

    @property
    def amount_with_internet_charges(self):
        total = self.amount_with_gst
        total += self.internet_charges

        return math.ceil(total)

    @property
    def get_total(self):
        total = self.amount_with_internet_charges
        return math.ceil(total)

    @property
    def ordered_products_count(self):
        return self.products.count()

    class Meta:
        verbose_name_plural = 'Orders'

    @property
    def get_json(self):
        return {
            "total_amount": self.get_total,
            "products_amount": self.products_amount,
            "amount_with_delivery": self.amount_with_delivery,
            "delivery_charges": self.delivery_charges,
            "gst": GST_CHARGES,
            "internet_charges": INTERNET_HANDLING_CHARGES,
            "amount_with_gst": self.amount_with_gst,
            "gst_amount": self.gst_amount,
            "internet_charges": self.internet_charges,
            "amount_with_internet_charges": self.amount_with_internet_charges,
            "gateway_order_id": self.gateway_order_id,
            "order_id": self.gateway_order_id,
            "id": self.id,
            "ordered_date": self.ordered_date,
            "updated_date": self.updated_date,
            "out_for_delivered": self.out_for_delivered,
            "delivered": self.received,
            "order_type": self.order_type,
            "payment_status": self.payment_status
        }


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.IntegerField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    default = models.BooleanField(default=False)

    @property
    def full_address(self):
        return f"{self.address} \n {self.area} \n {self.city} -  {self.state} \n  {self.country} - {self.pincode} \n Contact : {self.phone}"

    def __str__(self):
        return self.full_address

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    payment_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_response = JSONField(blank=True, null=True)

    def __str__(self):
        return self.payment_id


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"
