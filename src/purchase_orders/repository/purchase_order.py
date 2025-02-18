from purchase_orders.models import PurchaseOrder


class PurchaseOrderRepository:
    @staticmethod
    def get_by_id(purchase_order_id):
        """Fetch a purchase order by its ID."""
        try:
            return PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise ValueError("Purchase order not found")

    @staticmethod
    def create(order_data):
        """Create a new purchase order."""
        return PurchaseOrder.objects.create(**order_data)

    @staticmethod
    def update(purchase_order, updated_data):
        """Update an existing purchase order."""
        for key, value in updated_data.items():
            setattr(purchase_order, key, value)
        purchase_order.save()
        return purchase_order

    @staticmethod
    def cancel(purchase_order):
        """Cancel a purchase order (soft delete or update status)."""
        purchase_order.status = "Cancelled"
        purchase_order.save()
        return purchase_order

    @staticmethod
    def confirm(purchase_order):
        """Confirm a purchase order."""
        purchase_order.status = "Confirmed"
        purchase_order.save()
        return purchase_order

    @staticmethod
    def approve(purchase_order):
        """Approve a purchase order."""
        purchase_order.status = "Approved"
        purchase_order.save()
        return purchase_order
