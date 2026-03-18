from rest_framework import serializers
from .models import CartItem
from products.models import Product
from products.serializers import ProductSerializer


CART_MAX_QUANTITY = 10


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["product_id", "quantity", "product"]

    def get_product(self, obj):
        product = Product.objects.filter(id=obj.product_id, is_active=True).first()
        if not product:
            return None
        return ProductSerializer(product).data


class AddToCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, max_value=CART_MAX_QUANTITY, default=1)


class UpdateQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=CART_MAX_QUANTITY)
