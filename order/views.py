from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.http.request import QueryDict
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Order, OrderProduct, Address, Payment, PaymentStatus, OrderTypes
from django.contrib.auth.models import User
from django.db.models import Q
from menu.models import Product, Offer
from branch.models import Branch
from .serializers import OrderSerializer, OrderAddressSerializer
from .razorpay_adapter import razorpayAdapter, OrderDetail
from fcm_django.models import FCMDevice
import json


class OrderAddressView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user_id=user.id)
        return queryset

    serializer_class = OrderAddressSerializer

    # def post(self, request, *args, **kwargs):
    #     req_user = self.request.user
    #     print("req_user")
    #     print(req_user)
    #     user = User.objects.get(pk=req_user.id)
    #     print("user")
    #     print(req_user)
    #     kwargs = {"user" : req_user}
    #     # if not request.user == user.username:
    #     #     raise PermissionDenied("You cannot add address.")
    #     return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if type(request.data) == QueryDict:
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = False
        if type(request.data) == dict:
            request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class OrderAddressInstanceView(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(Q(user_id=user.id) & Q(id=self.kwargs["pk"]))
        return queryset

    serializer_class = OrderAddressSerializer


class OrderView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print(":: OrderView -> post -> is_valid")
            order_user = User.objects.get(pk=request.user.id)
            order_type = request.data.get("order_type")
            if not order_type:
                order_type = request.data.get("payment_type")

            newAddress = Address()
            newAddress.user = order_user
            shipping_address = request.data.get("shipping_address")
            newAddress.address = shipping_address.get('address')
            newAddress.area = shipping_address.get('area')
            newAddress.city = shipping_address.get('city')
            newAddress.state = shipping_address.get('state')
            newAddress.country = shipping_address.get('country')
            newAddress.pincode = shipping_address.get('pincode')
            newAddress.phone = shipping_address.get('phone')

            # if True:
            #     return Response(newAddress.full_address, status=status.HTTP_200_OK)

            newAddress.save()

            print("::: newAddress :::")
            print(newAddress.pincode)

            new_order = Order()
            new_order.user = order_user
            new_order.shipping_address = newAddress
            new_order.order_type = order_type
            new_order.delivery_charges = 0
            branch = Branch.objects.get(pk=1)
            if branch and order_type == OrderTypes.DELIVERY:
                new_order.delivery_charges = branch.delivery_charges

            # if True:
            #     return Response(new_order.user.username, status=status.HTTP_200_OK)

            new_order.save()
            print("::: new_order :::")
            print(new_order)

            order_products = request.data.get("products")
            for product in order_products:
                print(product)
                iProduct = Product.objects.get(id=product["id"])
                # if True:
                #     return Response(iProduct.product, status=status.HTTP_200_OK)

                order_product = OrderProduct()
                order_product.user = order_user
                order_product.ordered = True
                order_product.quantity = product["quantity"]
                order_product.product = iProduct
                order_product.per_price = iProduct.current_price
                order_product.save()

                if "offer" in product.keys():
                    iOffer = Offer.objects.get(id=product["offer"])
                    order_product.offer = iOffer
                    order_product.save()

                new_order.products.add(order_product)

            new_order.save()
            new_order = Order.objects.get(pk=new_order.id)
            order_notes = {
                "phone": order_user.username,
                "order_type": order_type
            }

            # if payment_type == PaymentTypes.CASH_ON_DELIVERY:
            #     return Response(new_order.get_json, status=status.HTTP_201_CREATED)
            # else:
            order_details = OrderDetail(new_order.get_total,
                                        'order_' + str(new_order.id),
                                        order_notes)
            razorpay_order = razorpayAdapter.create_order(order_details)
            print(razorpay_order)

            new_order.gateway_order_id = razorpay_order.get("id")
            new_order.gateway_order_response = razorpay_order
            new_order.save()
            response_data = {
                'key': razorpayAdapter.key,
                'amount': razorpay_order.get(
                    "amount"),  #// in the smallest currency sub-unit.
                'order_id': razorpay_order.get("id"),
                "currency": razorpay_order.get("currency"),
                'prefill': {
                    'contact': order_user.username,
                    'email': order_user.email
                }
            }
            return Response(
                {
                    "order_info": new_order.get_json,
                    "order": order_details.json,
                    "payment_order": response_data
                },
                status=status.HTTP_201_CREATED)

            # device = FCMDevice.objects.filter(user=order_user).first()
            # if device:
            #     device.send_message("New order", "Your ordered placed")

        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # if pk:
        #     group = self.kwargs["uuid"]
        #     order = get_object_or_404(Order, pk=pk)
        #     serializer = OrderSerializer(order)
        #     return Response({"order": serializer.data})
        orders = Order.objects.filter(user__id=request.user.id, gateway_order_id__isnull=False).order_by('-ordered_date')
        serializer = OrderSerializer(orders, many=True)
        # print(serializer.data)
        print("values_list('name', 'email')")
        print(orders)
        # result = {"ordered" : orders[0][0], "ordered_date" : orders[0][1]}
        return Response({"orders": serializer.data})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class GetOrderStatusApi(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(
            gateway_order_id=self.kwargs["order_id"])
        return queryset

    def get(self, request, order_id, format=None):
        """
        Get Order Status
        """
        order = self.get_queryset().first()
        gateway_order= {}
        payment = {}
        gateway_payments = {}
        payment_response = {}
        order_status= None
        if order:
            gateway_order = razorpayAdapter.fetch_order(order_id)
            if gateway_order:
                order_status = gateway_order.get("status")
                if order_status == "paid":
                    order.payment_status = PaymentStatus.PAID
                    order.save()
                    payment = Payment.objects.filter(order=order).first()
                    if not payment:
                        gateway_payments = razorpayAdapter.fetch_order_payments(
                            order_id).get("items")
                        if len(gateway_payments) > 0:
                            payment_response = gateway_payments[0]
                            payment = Payment()
                            payment.order = order
                            payment.amount = payment_response.get("amount")
                            payment_response = json.dumps(payment_response),
                            payment.save()

        return Response({
            "order": order.get_json,
            "order_status": order_status,
            "gateway_order": gateway_order,
            "gateway_payments": gateway_payments,
            "payment_response": payment_response,
        })
