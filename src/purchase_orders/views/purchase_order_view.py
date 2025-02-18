from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from purchase_orders.serializers.purchase_order_serializers import (
    PurchaseOrderSerializer,
)
from purchase_orders.service.purchase_order_service import PurchaseOrderService
from core.helpers import generate_purchase_order_pdf, send_purchase_order_email
from user.models import CustomUser
from rest_framework.views import APIView


class PurchaseOrderView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.purchase_order_service = PurchaseOrderService()

    def post(self, request, *args, **kwargs):
        # Deserialize request data
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            order_data = serializer.validated_data

            try:
                # Create the purchase order
                purchase_order = self.purchase_order_service.create_purchase_order(
                    request=request,
                    order_data=order_data,
                    user=request.user,
                )

                # Generate the PDF for the created purchase order
                pdf_path = generate_purchase_order_pdf(purchase_order.po_number)

                vendor_email = purchase_order.vendor.email

                # Send email notification to vendor with the PDF
                send_purchase_order_email(
                    purchase_order, pdf_path, to_emails=[vendor_email]
                )

                # Notify COO and MD based on product price
                total_price = purchase_order.total_price

                coo_user = CustomUser.objects.get(role="COO")
                coo_email = coo_user.email
                md_user = CustomUser.objects.get(role="MD")
                md_email = md_user.email

                if total_price > 50000:
                    if coo_email:
                        send_purchase_order_email(
                            purchase_order, pdf_path, to_emails=[coo_email]
                        )
                    if md_email:
                        send_purchase_order_email(
                            purchase_order, pdf_path, to_emails=[md_email]
                        )
                else:
                    if coo_email:
                        send_purchase_order_email(
                            purchase_order, pdf_path, to_emails=[coo_email]
                        )

                return Response(
                    {
                        "message": "Purchase order created and notifications sent successfully!"
                    },
                    status=status.HTTP_201_CREATED,
                )

            except PermissionDenied as e:
                return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            # Update the purchase order
            updated_order = self.purchase_order_service.update_purchase_order(
                user=request.user, purchase_order_id=pk, updated_data=request.data
            )
            return Response(
                {
                    "message": "Purchase order updated successfully!",
                    "data": updated_order.id,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, *args, **kwargs):
        try:
            # Cancel the purchase order
            canceled_order = self.purchase_order_service.cancel_purchase_order(
                user=request.user, purchase_order_id=pk
            )
            return Response(
                {
                    "message": "Purchase order canceled successfully!",
                    "data": canceled_order.id,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk, *args, **kwargs):
        try:
            # Confirm the purchase order
            confirmed_order = self.purchase_order_service.confirm_purchase_order(
                user=request.user, purchase_order_id=pk
            )
            return Response(
                {
                    "message": "Purchase order confirmed successfully!",
                    "data": confirmed_order.id,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def approve(self, request, pk, *args, **kwargs):
        try:
            # Approve the purchase order
            approved_order = self.purchase_order_service.approve_purchase_order(
                user=request.user, purchase_order_id=pk
            )
            return Response(
                {
                    "message": "Purchase order approved successfully!",
                    "data": approved_order.id,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, pk, *args, **kwargs):
        try:
            # View the purchase order
            order = self.purchase_order_service.view_purchase_order(
                user=request.user, purchase_order_id=pk
            )
            return Response(
                {"message": "Purchase order details", "data": order},
                status=status.HTTP_200_OK,
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
