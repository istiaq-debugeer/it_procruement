# purchase_order/models.py
from core.abstract_model import CommonClass
from django.db import models
from user.models import CustomUser
import uuid


class Vendor(CommonClass):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(CommonClass):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PurchaseOrder(CommonClass):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    po_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_orders"
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")
    qtn_ref = models.CharField(max_length=100, blank=True, null=True)
    bill_to_name = models.CharField(max_length=255)
    bill_to_address = models.TextField()
    bill_to_phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    subject_description = models.TextField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=5, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    total_in_words = models.CharField(max_length=255)
    terms_and_conditions = models.TextField()
    payment_terms = models.TextField()
    delivery_location = models.TextField()
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_phone = models.CharField(max_length=20)
    company_email = models.EmailField()
    manager_name = models.CharField(max_length=255)
    md_name = models.CharField(max_length=255)

    def __str__(self):
        return f"PO {self.po_number}"


class PurchaseOrderItem(CommonClass):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    approved_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="approved_orders"
    )
    approval_type = models.CharField(max_length=50)
    approved_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
