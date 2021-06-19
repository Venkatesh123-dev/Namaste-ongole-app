import random
from rest_framework import generics, viewsets
from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny


from .models import *
from .serializers import *


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()


class OfferList(generics.ListAPIView):
    queryset = Offer.objects.filter(is_enabled=True)
    serializer_class = OfferSerializer
    permission_classes = ()


class ProductList(generics.ListAPIView):
    def get_queryset(self):
        queryset = Product.objects.filter(category_id=self.kwargs["pk"])
        return queryset
    serializer_class = ProductSerializer
    permission_classes = ()


class AddCategory(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()

class AddProduct(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()



class RandomProducts(generics.ListAPIView):
    def get_queryset(self):
        queryset = Product.objects.all().order_by('?')[:10]
        return queryset
    serializer_class = ProductSerializer
    permission_classes = ()
 




# class ProductOptionsList(generics.ListAPIView):
#     queryset = ProductOptions.objects.all()
#     serializer_class = ProductOptionsSerializer
#     permission_classes = (AllowAny,)

