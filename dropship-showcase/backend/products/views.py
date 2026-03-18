from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.filter(is_active=True)

    category = request.query_params.get("category")
    if category:
        products = products.filter(category__icontains=category)

    brand = request.query_params.get("brand")
    if brand:
        products = products.filter(brand__icontains=brand)

    search = request.query_params.get("q")
    if search:
        products = products.filter(name__icontains=search)

    return Response({"products": ProductSerializer(products, many=True).data})


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response({"product": ProductSerializer(product).data})
