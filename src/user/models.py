from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid


class CustomUser(AbstractUser):
    ROLES = (
        ("PROCUREMENT", "Procurement Team"),
        ("COO", "Chief Operating Officer"),
        ("MD", "Managing Director"),
        ("VENDOR", "Vendor"),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, choices=ROLES)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Override groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions", blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
