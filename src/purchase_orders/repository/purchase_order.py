from purchase_orders.models import PurchaseOrder


class PurchaseOrderRepository:
    @staticmethod
    def get_by_id(purchase_order_id):

        try:
            return PurchaseOrder.objects.get(id=purchase_order_id)
        except PurchaseOrder.DoesNotExist:
            raise ValueError("Purchase order not found")

    @staticmethod
    def create(order_data):

        return PurchaseOrder.objects.create(**order_data)

    @staticmethod
    def update(purchase_order, updated_data):

        for key, value in updated_data.items():
            setattr(purchase_order, key, value)
        purchase_order.save()
        return purchase_order

    @staticmethod
    def cancel(purchase_order):

        purchase_order.status = "Cancelled"
        purchase_order.save()
        return purchase_order

    @staticmethod
    def confirm(purchase_order):

        purchase_order.status = "Confirmed"
        purchase_order.save()
        return purchase_order

    @staticmethod
    def approve(purchase_order):

        purchase_order.status = "Approved"
        purchase_order.save()
        return purchase_order
