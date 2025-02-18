# purchase_order/models.py
from core.abstract_model import CommonClass
from django.db import models
from user.models import CustomUser


class Vendor(CommonClass):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(CommonClass):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PurchaseOrder(CommonClass):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
    po_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_orders"
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"PO {self.po_number}"


class PurchaseOrderItem(CommonClass):
    uuid = models.UUIDField(primary_key=True, editable=False, unique=True)
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
