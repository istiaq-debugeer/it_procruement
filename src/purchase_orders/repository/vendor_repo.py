# purchase_order/repositories.py
from models import Vendor


class VendorRepository:
    def get_all_vendors(self):

        return Vendor.objects.all()

    def get_vendor_by_uuid(self, uuid):

        return Vendor.objects.get(uuid=uuid)

    def create_vendor(self, data):

        return Vendor.objects.create(**data)

    def update_vendor(self, uuid, data):

        vendor = self.get_vendor_by_uuid(uuid)
        for key, value in data.items():
            setattr(vendor, key, value)
        vendor.save()
        return vendor

    def delete_vendor(self, uuid):

        vendor = self.get_vendor_by_uuid(uuid)
        vendor.delete()
