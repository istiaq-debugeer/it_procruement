# purchase_order/views.py
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service.product_service import ProductService
from serializers.product_serializers import ProductSerializer


class ProductCreateView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            service = ProductService()
            try:
                product = service.create_product(serializer.validated_data)
                return Response(
                    ProductSerializer(product).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
