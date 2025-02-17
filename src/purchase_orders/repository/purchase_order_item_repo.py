# purchase_order/repositories.py
from models import PurchaseOrderItem


class PurchaseOrderItemRepository:
    def get_all_purchase_order_items(self):
        return PurchaseOrderItem.objects.all()

    def get_purchase_order_item_by_uuid(self, uuid):
        return PurchaseOrderItem.objects.get(uuid=uuid)

    def create_purchase_order_item(self, data):

        return PurchaseOrderItem.objects.create(**data)

    def update_purchase_order_item(self, uuid, data):

        item = self.get_purchase_order_item_by_uuid(uuid)
        for key, value in data.items():
            setattr(item, key, value)
        item.save()
        return item

    def delete_purchase_order_item(self, uuid):

        item = self.get_purchase_order_item_by_uuid(uuid)
        item.delete()
