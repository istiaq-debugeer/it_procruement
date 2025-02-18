from datetime import datetime

from django.db import models


class CommonClass(models.Model):
    is_delete = models.BooleanField(default=False, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_delete = True
        self.deleted_at = datetime.now()
        self.save()

    def restore(self):
        self.is_delete = False
        self.deleted_at = None
        self.save()
