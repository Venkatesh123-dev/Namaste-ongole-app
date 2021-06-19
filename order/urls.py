from django.urls import path
from .views import *


urlpatterns = [
    path('order/', OrderView.as_view(), name="order"),
    path('address/', OrderAddressView.as_view(), name="address_post"),
    path('address/<int:pk>', OrderAddressInstanceView.as_view(), name="address"),
    path('order/<str:order_id>', GetOrderStatusApi.as_view(), name="get_order_status"),
]

