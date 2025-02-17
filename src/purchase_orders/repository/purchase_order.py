# purchase_order/repositories.py
from models import PurchaseOrder


class PurchaseOrderRepository:
    def get_all_purchase_orders(self):
        return PurchaseOrder.objects.all()

    def get_purchase_order_by_uuid(self, uuid):
        return PurchaseOrder.objects.get(uuid=uuid)

    def create_purchase_order(self, data):
        return PurchaseOrder.objects.create(**data)

    def update_purchase_order(self, uuid, data):
        purchase_order = self.get_purchase_order_by_uuid(uuid)
        for key, value in data.items():
            setattr(purchase_order, key, value)
        purchase_order.save()
        return purchase_order

    def delete_purchase_order(self, uuid):
        purchase_order = self.get_purchase_order_by_uuid(uuid)
        purchase_order.delete()
