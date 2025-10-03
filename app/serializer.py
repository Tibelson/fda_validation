from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    approved = serializers.BooleanField(read_only=True)
    expiry_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)

    class Meta:
        model = Product
        fields = [
            'name',
            'company',
            'barcode',
            'product_id',
            'batch_code',
            'category',
            'expiry_date',
            'approved',
        ]
