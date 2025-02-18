# purchase_order/serializers.py
from rest_framework import serializers

from purchase_orders.models import PurchaseOrderItem


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = [
            "uuid",
            "purchase_order",
            "product",
            "quantity",
            "unit_price",
            "approved_by",
            "approval_type",
            "approved_at",
            "comments",
        ]

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_unit_price(self, value):
        """Validate that the unit price is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than zero.")
        return value
