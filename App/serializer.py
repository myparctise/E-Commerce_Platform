from dataclasses import fields
from rest_framework import serializers
from .models import *

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_details
        fields = "__all__"

class show_product_serializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product_details
        fields = "__all__"