# purchase_order/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .services import PurchaseOrderItemService
from .serializers import PurchaseOrderItemSerializer


class PurchaseOrderItemCreateView(APIView):
    def post(self, request):
        serializer = PurchaseOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            service = PurchaseOrderItemService()
            try:
                item = service.create_purchase_order_item(serializer.validated_data)
                return Response(
                    PurchaseOrderItemSerializer(item).data,
                    status=status.HTTP_201_CREATED,
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderItemDetailView(APIView):
    def get(self, request, uuid):
        service = PurchaseOrderItemService()
        try:
            item = service.get_purchase_order_item(uuid)
            return Response(
                PurchaseOrderItemSerializer(item).data, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        serializer = PurchaseOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            service = PurchaseOrderItemService()
            try:
                item = service.update_purchase_order_item(
                    uuid, serializer.validated_data
                )
                return Response(
                    PurchaseOrderItemSerializer(item).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        service = PurchaseOrderItemService()
        try:
            service.delete_purchase_order_item(uuid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderItemListView(APIView):
    def get(self, request):
        service = PurchaseOrderItemService()
        items = service.get_all_purchase_order_items()
        serializer = PurchaseOrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
