from django.shortcuts import render
from rest_framework import serializers
from .models import Branch
# Create your views here.


class BranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, default="Namaste Ongole")
    area = serializers.CharField(max_length=100, default="Kothapatnam (m) pallepalem (v)")
    city = serializers.CharField(max_length=20, default="Ongole")
    state = serializers.CharField(max_length=100, default="Andhra Pradesh")
    country = serializers.CharField(max_length=100, default="India")
    pincode = serializers.CharField(max_length=100)
    start_time = serializers.TimeField()
    close_time = serializers.TimeField()
    gst = serializers.IntegerField(default=5)
    delivery_charges = serializers.IntegerField(default=25)

    class Meta:
        model = Branch
        fields = '__all__'
        # fields = ('address', 'area', 'city','state', 'country', 'pincode')
