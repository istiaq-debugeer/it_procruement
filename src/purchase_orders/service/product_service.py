# purchase_order/services.py
from django.core.exceptions import ValidationError

from purchase_orders.repository.product_repo import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()

    def create_product(self, data):

        # Validate unit price
        if data.get("unit_price", 0) <= 0:
            raise ValidationError("Unit price must be greater than zero.")

        # Add default description if none is provided
        if "description" not in data or not data["description"]:
            data["description"] = "No description provided."

        return self.product_repo.create_product(data)

    def update_product(self, uuid, data):

        product = self.product_repo.get_product_by_uuid(uuid)
        if not product:
            raise ValidationError("Product not found.")

        # Validate unit price
        if "unit_price" in data and data["unit_price"] <= 0:
            raise ValidationError("Unit price must be greater than zero.")

        # Update the product
        return self.product_repo.update_product(uuid, data)

    def delete_product(self, uuid):

        product = self.product_repo.get_product_by_uuid(uuid)
        if not product:
            raise ValidationError("Product not found.")

        # Check if the product can be deleted (e.g., based on status)
        if product.status == "Archived":
            raise ValidationError("Archived products cannot be deleted.")

        # Delete the product
        self.product_repo.delete_product(uuid)

    def get_product(self, uuid):

        product = self.product_repo.get_product_by_uuid(uuid)
        if not product:
            raise ValidationError("Product not found.")
        return product

    def get_all_products(self):

        return self.product_repo.get_all_products()
