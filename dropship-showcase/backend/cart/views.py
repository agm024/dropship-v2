from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartItem
from .serializers import (
    CART_MAX_QUANTITY,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateQuantitySerializer,
)
from products.models import Product


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_list(request):
    user = request.user

    if request.method == "GET":
        items = CartItem.objects.filter(user=user)
        return Response({"items": CartItemSerializer(items, many=True).data})

    if request.method == "POST":
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        product_id = serializer.validated_data["productId"]
        quantity = serializer.validated_data["quantity"]

        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        max_allowed = min(CART_MAX_QUANTITY, int(product.stock or 0))
        if max_allowed < 1:
            return Response(
                {"errors": {"quantity": ["This product is out of stock."]}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        item, created = CartItem.objects.get_or_create(
            user=user,
            product_id=product_id,
            defaults={"quantity": quantity},
        )

        new_quantity = quantity if created else (item.quantity + quantity)
        if new_quantity > max_allowed:
            return Response(
                {
                    "errors": {
                        "quantity": [
                            f"Maximum allowed quantity is {max_allowed} for this product."
                        ]
                    }
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if not created:
            item.quantity = new_quantity
            item.save(update_fields=["quantity"])

        return Response({"item": CartItemSerializer(item).data}, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        CartItem.objects.filter(user=user).delete()
        return Response({"success": True})


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_item(request, product_id):
    user = request.user

    if request.method == "PUT":
        serializer = UpdateQuantitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            item = CartItem.objects.get(user=user, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        max_allowed = min(CART_MAX_QUANTITY, int(product.stock or 0))
        quantity = serializer.validated_data["quantity"]
        if max_allowed < 1:
            return Response(
                {"errors": {"quantity": ["This product is out of stock."]}},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        if quantity > max_allowed:
            return Response(
                {
                    "errors": {
                        "quantity": [
                            f"Maximum allowed quantity is {max_allowed} for this product."
                        ]
                    }
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return Response({"item": CartItemSerializer(item).data})

    if request.method == "DELETE":
        CartItem.objects.filter(user=user, product_id=product_id).delete()
        return Response({"success": True})
