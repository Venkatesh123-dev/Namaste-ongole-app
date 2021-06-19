from rest_framework import serializers

from .models import Order,OrderProduct, Address


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderProduct
        fields = '__all__'

    def to_representation(self, instance):
        return instance.get_json

class OrderAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = ('id', 'user', 'address', 'area', 'city','state', 'country', 'pincode')
        extra_kwargs = {"user": {"required": False, "allow_null": True}}



class OrderSerializer(serializers.Serializer):
    products = OrderProductSerializer(many=True)
    shipping_address = OrderAddressSerializer()
    order_type = serializers.IntegerField()

    def validate(self, attrs):
        errors = {}
        if not attrs.get("products"):
            errors['products'] = ["Products should not be empty"]
            raise serializers.ValidationError(errors)
        


        return super().validate(attrs)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print(":: OrderSerializer -> create")
        order = Order()
        # order = Orders.objects.create(**validated_data)
        order.save()
        return order

    class Meta:
        model = Order
        fields = ["products"]

    def to_representation(self, instance):
        products = [ product.get_json for product in instance.products.all()]
        total_amount = sum([product.get("total_price") for product in products ])
        return {
            "total_amount": total_amount,
            "products": products,
            "shipping_address": instance.shipping_address.full_address,
            "order" : instance.get_json,
            "order_id" : instance.id
        }
