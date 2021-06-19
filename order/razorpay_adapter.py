import razorpay
import json
from django.conf import settings
from json import JSONEncoder
from dataclasses import dataclass
from django.core.serializers.json import DjangoJSONEncoder
# client = razorpay.Client(auth=("<YOUR_KEY>", "<YOUR_SECRET>"))


@dataclass(frozen=True)
class OrderDetail():
    amount: int
    currency = 'INR'
    receipt: str
    payment_capture = 1
    notes: dict

    @property
    def json(self):
        return self.data

    @property
    def data(self):
        return {
            "amount": self.amount * 100,
            "currency": self.currency,
            "receipt": self.receipt,
            "payment_capture": self.payment_capture,
            "notes": {
                "data": json.dumps(self.notes, indent=4)
            }
        }


class OrderEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class RazorpayAdapter():
    key = 'RAZORPAY_KEY'
    secret ='RAZORPAY_SECRET'

    def __init__(self):
        self.client = razorpay.Client(auth=(self.key, self.secret))

    def create_order(self, order_details: OrderDetail):
        order = self.client.order.create(data=order_details.data)
        try:
            return self.client.order.create(data=order_details.data)
        except:
            return self.client.order.create(data=order_details.data)

    def fetch_order(self, order_id):
        if order_id:
            try:
                return self.client.order.fetch(order_id)
            except:
                return self.client.order.fetch(order_id)

        return None

    def fetch_order_payments(self, order_id):
        if order_id:
            try:
                return self.client.order.fetch_all_payments(order_id)
            except:
                return self.client.order.fetch_all_payments(order_id)
        return None


razorpayAdapter = RazorpayAdapter()
