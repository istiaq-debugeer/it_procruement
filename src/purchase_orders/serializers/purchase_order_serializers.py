from rest_framework import serializers
from user.models import CustomUser as CustomUser

from purchase_orders.models import PurchaseOrder
from purchase_orders.models import Vendor as Vendor


class PurchaseOrderSerializer(serializers.ModelSerializer):

    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    # def validate(self, data):

    #     data["total_price"] = data["quantity"] * data["price"]
    #     return data
