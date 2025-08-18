from rest_framework import serializers
from goods.models import ProductModel


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "title", "description", "price"]
