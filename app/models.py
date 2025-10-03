from django.db import models

from django.db import models

class Product(models.Model):
    client_name = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_category = models.CharField(max_length=255, null=True, blank=True)
    expiry_date = models.CharField(max_length=50, null=True, blank=True)  # keep as text for now
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.client_name})"


