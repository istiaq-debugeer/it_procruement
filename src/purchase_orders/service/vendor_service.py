# purchase_order/services.py
from rest_framework.exceptions import ValidationError
from .repositories import VendorRepository


class VendorService:
    def __init__(self):
        self.vendor_repo = VendorRepository()

    def create_vendor(self, data):

        # Validate phone and email
        if not data.get("phone"):
            raise ValidationError("Phone number cannot be empty.")
        if not data.get("email"):
            raise ValidationError("Email cannot be empty.")

        # Save the vendor
        return self.vendor_repo.create_vendor(data)

    def update_vendor(self, uuid, data):

        vendor = self.vendor_repo.get_vendor_by_uuid(uuid)
        if not vendor:
            raise ValidationError("Vendor not found.")

        # Validate phone and email
        if "phone" in data and not data["phone"]:
            raise ValidationError("Phone number cannot be empty.")
        if "email" in data and not data["email"]:
            raise ValidationError("Email cannot be empty.")

        # Update the vendor
        return self.vendor_repo.update_vendor(uuid, data)

    def delete_vendor(self, uuid):

        vendor = self.vendor_repo.get_vendor_by_uuid(uuid)
        if not vendor:
            raise ValidationError("Vendor not found.")

        # Delete the vendor
        self.vendor_repo.delete_vendor(uuid)

    def get_vendor(self, uuid):

        vendor = self.vendor_repo.get_vendor_by_uuid(uuid)
        if not vendor:
            raise ValidationError("Vendor not found.")
        return vendor

    def get_all_vendors(self):

        return self.vendor_repo.get_all_vendors()
