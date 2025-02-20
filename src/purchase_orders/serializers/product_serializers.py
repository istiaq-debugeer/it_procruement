# purchase_order/serializers.py
from rest_framework import serializers

from purchase_orders.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["uuid", "name", "description", "unit_price"]

    def validate_unit_price(self, value):

        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than zero.")
        return value
