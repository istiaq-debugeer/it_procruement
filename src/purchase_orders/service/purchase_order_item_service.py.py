# purchase_order/services.py
from rest_framework.exceptions import ValidationError
from repository.purchase_order_item_repo import PurchaseOrderItemRepository


class PurchaseOrderItemService:
    def __init__(self):
        self.purchase_order_item_repo = PurchaseOrderItemRepository()

    def create_purchase_order_item(self, data):
        if data.get("quantity", 0) <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if data.get("unit_price", 0) <= 0:
            raise ValidationError("Unit price must be greater than zero.")

        return self.purchase_order_item_repo.create_purchase_order_item(data)

    def update_purchase_order_item(self, uuid, data):
        item = self.purchase_order_item_repo.get_purchase_order_item_by_uuid(uuid)
        if not item:
            raise ValidationError("Purchase order item not found.")

        if "quantity" in data and data["quantity"] <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if "unit_price" in data and data["unit_price"] <= 0:
            raise ValidationError("Unit price must be greater than zero.")

        return self.purchase_order_item_repo.update_purchase_order_item(uuid, data)

    def delete_purchase_order_item(self, uuid):
        item = self.purchase_order_item_repo.get_purchase_order_item_by_uuid(uuid)
        if not item:
            raise ValidationError("Purchase order item not found.")
        self.purchase_order_item_repo.delete_purchase_order_item(uuid)

    def get_purchase_order_item(self, uuid):
        item = self.purchase_order_item_repo.get_purchase_order_item_by_uuid(uuid)
        if not item:
            raise ValidationError("Purchase order item not found.")
        return item

    def get_all_purchase_order_items(self):

        return self.purchase_order_item_repo.get_all_purchase_order_items()
