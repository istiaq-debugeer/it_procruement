from rest_framework import serializers
from user.models import CustomUser as CustomUser

from purchase_orders.models import PurchaseOrder
from purchase_orders.models import Vendor as Vendor


class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = [
            'po_number',      
            'item',           
            'quantity',       
            'price',         
            'vendor',         
            'created_by',     
            'order_date',     
            'status',         
            'total_price',    
        ]
        read_only_fields = ['po_number', 'created_by', 'order_date']  

    def validate(self, data):
        
        data['total_price'] = data['quantity'] * data['price']
        return data
