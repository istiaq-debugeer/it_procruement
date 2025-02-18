from django.core.exceptions import PermissionDenied

from purchase_orders.models import Vendor
from purchase_orders.repository.purchase_order import PurchaseOrderRepository
from user.models import CustomUser


class PurchaseOrderService:

    def __init__(self):
        self.repo = PurchaseOrderRepository()

    def create_purchase_order(self, request, order_data, user):
        # Check if the user is an instance of CustomUser
        if isinstance(request.user, CustomUser):
            # Check if the user is in the PROCUREMENT group
            if not request.user.groups.filter(name="PROCUREMENT").exists():
                raise PermissionDenied(
                    "You do not have permission to create a purchase order."
                )

            # Alternatively, can check for the permission directly
            if not request.user.has_perm("purchase_orders.add_purchaseorder"):
                raise PermissionDenied(
                    "You do not have permission to create a purchase order."
                )

        # Create the purchase order using the repository
        purchase_order = self.repo.create(order_data)

        return purchase_order

    def update_purchase_order(self, user, request, purchase_order_id, updated_data):
        purchase_order = self.repo.get_by_id(purchase_order_id)

        if isinstance(request.user, CustomUser):
            if not request.user.groups.filter(name="PROCUREMENT").exists():
                raise PermissionDenied(
                    "You do not have permission to update this purchase order."
                )
            # Check if the user has permission to change purchase orders (Procurement Team)
            if not user.has_perm("purchase_orders.change_purchaseorder"):
                raise PermissionDenied(
                    "You do not have permission to update this purchase order."
                )

        # Update the purchase order using the repository
        updated_order = self.repo.update(purchase_order, updated_data)
        return updated_order

    def cancel_purchase_order(self, user, request, purchase_order_id):
        purchase_order = self.repo.get_by_id(purchase_order_id)

        if isinstance(request.user, CustomUser):
            # Check if the user has permission to delete purchase orders (Procurement Team)
            if not user.has_perm("purchase_orders.delete_purchaseorder"):
                raise PermissionDenied(
                    "You do not have permission to cancel this purchase order."
                )

            # Cancel the purchase order using the repository
            canceled_order = self.repo.cancel(purchase_order)
            return canceled_order

    def confirm_purchase_order(self, user, request, purchase_order_id):
        purchase_order = self.repo.get_by_id(purchase_order_id)

        if isinstance(request.user, CustomUser):
            # Check if the user is COO and has permission to confirm purchase orders
            if not user.groups.filter(name="COO").exists():
                raise PermissionDenied("Only the COO can confirm this purchase order.")
        # Check if the user is COO and has permission to confirm purchase orders
        if not user.has_perm("purchase_orders.confirm_purchaseorder"):
            raise PermissionDenied("Only the COO can confirm this purchase order.")

        # Confirm the purchase order using the repository
        confirmed_order = self.repo.confirm(purchase_order)
        return confirmed_order

    def approve_purchase_order(self, user, purchase_order_id):
        purchase_order = self.repo.get_by_id(purchase_order_id)

        if isinstance(request.user, CustomUser):
            # Check if the user is MD and has permission to approve purchase orders
            if not user.groups.filter(name="MD").exists():
                raise PermissionDenied(
                    "Only the Managing Director can approve this purchase order."
                )
        # Check if the user is MD and has permission to approve purchase orders
        if not user.has_perm("purchase_orders.approve_purchaseorder"):
            raise PermissionDenied(
                "Only the Managing Director can approve this purchase order."
            )

        # Approve the purchase order using the repository
        approved_order = self.repo.approve(purchase_order)
        return approved_order

    def view_purchase_order(self, user, purchase_order_id):
        # Fetch the purchase order
        purchase_order = self.repo.get_by_id(purchase_order_id)

        # Check if the user is associated with a vendor
        if hasattr(user, "vendor"):
            # Check if the vendor is associated with the purchase order
            if purchase_order.vendor != user.vendor:
                raise PermissionDenied(
                    "You do not have permission to view this purchase order."
                )
        else:
            # For non-vendor users, check if they have the 'view_purchaseorder' permission
            if not user.has_perm("purchase_orders.view_purchaseorder"):
                raise PermissionDenied(
                    "You do not have permission to view this purchase order."
                )

        return purchase_order
