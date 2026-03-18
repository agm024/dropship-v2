from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "short_description",
            "price",
            "category",
            "brand",
            "product_code",
            "image_url",
            "gallery_urls",
            "features",
            "stock",
            "rating",
            "is_active",
            "created_at",
            "updated_at",
        ]
