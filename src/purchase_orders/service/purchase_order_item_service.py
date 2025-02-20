from django.core.exceptions import PermissionDenied

from purchase_orders.models import PurchaseOrder


class PurchaseOrderService:

    def create_purchase_order(self, user, order_data):
        # Check if the user has the permission to add purchase orders (Procurement Team)
        if not user.has_perm('purchase_orders.add_purchaseorder'):
            raise PermissionDenied("You do not have permission to create a purchase order.")

        # Proceed to create the purchase order if the user has permission
        purchase_order = PurchaseOrder.objects.create(**order_data)
        return purchase_order

    def update_purchase_order(self, user, purchase_order_id, updated_data):
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        
        # Check if the user has permission to change purchase orders (Procurement Team)
        if not user.has_perm('purchase_orders.change_purchaseorder'):
            raise PermissionDenied("You do not have permission to update this purchase order.")
        
        # Update the purchase order
        for key, value in updated_data.items():
            setattr(purchase_order, key, value)
        
        purchase_order.save()
        return purchase_order

    def cancel_purchase_order(self, user, purchase_order_id):
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
        
        # Check if the user has permission to delete purchase orders (Procurement Team)
        if not user.has_perm('purchase_orders.delete_purchaseorder'):
            raise PermissionDenied("You do not have permission to cancel this purchase order.")
        
        # Cancel the purchase order (soft delete or update status)
        purchase_order.status = "Cancelled"
        purchase_order.save()
        return purchase_order

    def confirm_purchase_order(self, user, purchase_order_id):
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

        # Check if the user is COO and has permission to confirm purchase orders
        if not user.has_perm('purchase_orders.confirm_purchaseorder'):
            raise PermissionDenied("Only the COO can confirm this purchase order.")
        
        # Confirm the purchase order
        purchase_order.status = "Confirmed"
        purchase_order.save()
        return purchase_order

    def approve_purchase_order(self, user, purchase_order_id):
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

        # Check if the user is MD and has permission to approve purchase orders
        if not user.has_perm('purchase_orders.approve_purchaseorder'):
            raise PermissionDenied("Only the Managing Director can approve this purchase order.")
        
        # Approve the purchase order
        purchase_order.status = "Approved"
        purchase_order.save()
        return purchase_order

    def view_purchase_order(self, user, purchase_order_id):
        purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)

        # Check if the user has permission to view purchase orders (All groups have view permission)
        if not user.has_perm('purchase_orders.view_purchaseorder'):
            raise PermissionDenied("You do not have permission to view this purchase order.")
        
        return purchase_order
