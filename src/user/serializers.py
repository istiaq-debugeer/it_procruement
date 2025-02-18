# user/serializers.py
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "uuid",
            "username",
            "email",
            "role",
            "phone",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {"write_only": True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            role=validated_data.get("role", "PROCUREMENT"),  # Default role
            phone=validated_data.get("phone", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.role = validated_data.get("role", instance.role)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        # Handle password update
        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance
