from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from purchase_orders.models import PurchaseOrder

# Get the content type for the PurchaseOrder model
content_type = ContentType.objects.get_for_model(PurchaseOrder)

# Ensure permissions exist (or create them)
permissions = [
    ("view_purchaseorder", "Can view purchase order"),
    ("add_purchaseorder", "Can add purchase order"),
    ("change_purchaseorder", "Can change purchase order"),
    ("delete_purchaseorder", "Can delete purchase order"),
    ("confirm_purchaseorder", "Can confirm purchase order"),  # For COO
    ("approve_purchaseorder", "Can approve purchase order"),  # For MD
]

for codename, name in permissions:
    Permission.objects.get_or_create(
        codename=codename, content_type=content_type, defaults={"name": name}
    )

# Fetch permissions
view_permission = Permission.objects.get(codename="view_purchaseorder", content_type=content_type)
add_permission = Permission.objects.get(codename="add_purchaseorder", content_type=content_type)
change_permission = Permission.objects.get(codename="change_purchaseorder", content_type=content_type)
delete_permission = Permission.objects.get(codename="delete_purchaseorder", content_type=content_type)
confirm_permission = Permission.objects.get(codename="confirm_purchaseorder", content_type=content_type)
approve_permission = Permission.objects.get(codename="approve_purchaseorder", content_type=content_type)

# Create groups if they don’t exist
procurement_team, _ = Group.objects.get_or_create(name="Procurement Team")
coo, _ = Group.objects.get_or_create(name="COO")
md, _ = Group.objects.get_or_create(name="MD")
vendor, _ = Group.objects.get_or_create(name="Vendor")

# Assign permissions to groups
procurement_team.permissions.set([view_permission, add_permission, change_permission, delete_permission])

coo.permissions.set([view_permission, confirm_permission])  # COO can view and confirm purchase orders
md.permissions.set([view_permission, approve_permission])   # MD can view and approve purchase orders

vendor.permissions.set([])  # Vendors should only see their assigned orders via code logic

print("Permissions and groups assigned successfully!")
