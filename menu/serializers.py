from rest_framework import serializers

from .models import *




class ProductSerializer(serializers.ModelSerializer):
    # product_options = ProductOptionsSerializer(many=True, required=False)
    
    category_name = serializers.SerializerMethodField(method_name='categoryName')

    def categoryName(self, instance):
        return instance.category.category

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)
    exclude_products = ProductSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = '__all__'



# class ProductOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductOptions
#         fields = '__all__'
