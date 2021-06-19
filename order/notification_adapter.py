from fcm_django.models import FCMDevice
from django.core.serializers.json import DjangoJSONEncoder
import json


class NotificationAdapter():
    def send_order_updates(self, order):
        message = ''
        if order.order_placed:
            message = 'Your order is placed and We will notify orders\nThank you'

        if order.out_for_delivered:
            message = 'Your order is on the way...'

        if order.received:
            message = 'Your order has been delivered\nThank you'

        if len(message) > 0:
            device = FCMDevice.objects.filter(user=order.user)
            if device:
                products = [
                    product.get_json for product in order.products.all()
                ]
                total_amount = sum(
                    [product.get("total_price") for product in products])
                data = {
                    "total_amount":
                    total_amount,
                    "products":
                    products,
                    "shipping_address":
                    order.shipping_address.full_address,
                    "order_id": order.id
                }
                device.send_message(title="Order Details",
                                    body=message,
                                    data=data)


notificationManager = NotificationAdapter()