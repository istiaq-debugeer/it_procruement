# purchase_order/repositories.py
from models import Product


class ProductRepository:

    def create_product(self, data):
        return Product.objects.create(**data)

    def update_product(self, uuid, data):

        product = self.get_product_by_uuid(uuid)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    def get_all_products(self):
        return Product.objects.all()

    def get_product_by_uuid(self, uuid):

        return Product.objects.get(uuid=uuid)

    def delete_product(self, uuid):

        product = self.get_product_by_uuid(uuid)
        product.delete()
