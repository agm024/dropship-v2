from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_number",
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "rating",
        "is_active",
        "image_preview",
        "created_at",
    ]
    list_filter = ["is_active", "category", "brand", "created_at"]
    search_fields = ["name", "brand", "category", "product_code", "description"]
    list_editable = ["is_active", "stock", "price"]
    readonly_fields = ["product_number", "created_at", "updated_at", "image_preview_large"]
    ordering = ["-created_at"]
    fieldsets = (
        ("Basic Info", {
            "fields": ("product_number", "name", "brand", "category", "product_code", "is_active"),
        }),
        ("Pricing & Stock", {
            "fields": ("price", "stock", "rating"),
        }),
        ("Description", {
            "fields": ("short_description", "description", "features"),
        }),
        ("Images", {
            "fields": ("image_url", "image_preview_large", "gallery_urls"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:4px;" />',
                obj.image_url,
            )
        return "—"
    image_preview.short_description = "Image"

    def product_number(self, obj):
        return obj.id
    product_number.short_description = "Product #"

    def image_preview_large(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:300px;object-fit:contain;border-radius:8px;" />',
                obj.image_url,
            )
        return "No image"
    image_preview_large.short_description = "Image Preview"
