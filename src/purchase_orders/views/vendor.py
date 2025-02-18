# purchase_order/views.py
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from purchase_orders.serializers.vendor_serializers import VendorSerializer
from purchase_orders.service.vendor_service import VendorService


class VendorCreateView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            service = VendorService()
            try:
                vendor = service.create_vendor(serializer.validated_data)
                return Response(
                    VendorSerializer(vendor).data, status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    def get(self, request, uuid):
        service = VendorService()
        try:
            vendor = service.get_vendor(uuid)
            return Response(VendorSerializer(vendor).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            service = VendorService()
            try:
                vendor = service.update_vendor(uuid, serializer.validated_data)
                return Response(
                    VendorSerializer(vendor).data, status=status.HTTP_200_OK
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        service = VendorService()
        try:
            service.delete_vendor(uuid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class VendorListView(APIView):
    def get(self, request):
        service = VendorService()
        vendors = service.get_all_vendors()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
