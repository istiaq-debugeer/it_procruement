from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from purchase_orders.serializers.product_serializers import ProductSerializer
from purchase_orders.service.product_service import ProductService


class ProductView(APIView):
    def __init__(self, **kwargs):
        self.product_service = ProductService()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
       
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = self.product_service.create_product(serializer.validated_data)
                return Response({"message": "Product created successfully!", "data": product.id}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, uuid=None, *args, **kwargs):
        # Retrieve a product by UUID or get all products
        try:
            if uuid:
                product = self.product_service.get_product(uuid)
                serializer = ProductSerializer(product)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                products = self.product_service.get_all_products()
                serializer = ProductSerializer(products, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid, *args, **kwargs):
        """Update a product by UUID"""
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                product = self.product_service.update_product(uuid, serializer.validated_data)
                return Response({"message": "Product updated successfully!", "data": product.id}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, *args, **kwargs):
        """Delete a product by UUID"""
        try:
            self.product_service.delete_product(uuid)
            return Response({"message": "Product deleted successfully!"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
