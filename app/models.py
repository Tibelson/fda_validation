from django.db import models

from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)



class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50, unique=True)  # UPC/EAN/GTIN
    product_id = models.CharField(max_length=50, blank=True, null=True)
    batch_code = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="app")

    def __str__(self):
        return self.name

