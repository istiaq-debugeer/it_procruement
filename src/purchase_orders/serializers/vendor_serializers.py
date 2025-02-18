# purchase_order/serializers.py
from rest_framework import serializers

from purchase_orders.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "uuid",
            "name",
            "address",
            "phone",
            "email",
        ]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number cannot be empty.")
        # Add additional phone number validation logic if needed (e.g., regex for phone format)
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        # Add additional email validation logic if needed (e.g., regex for email format)
        return value

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
