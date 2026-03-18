from django.db import models
from django.db import transaction


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    short_description = models.CharField(max_length=500, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, default="")
    brand = models.CharField(max_length=100, blank=True, default="")
    product_code = models.CharField(max_length=100, blank=True, default="")
    image_url = models.URLField(max_length=1000, blank=True, default="")
    gallery_urls = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Reuse the smallest missing positive ID when creating a new product.
        if self.pk is None:
            with transaction.atomic():
                existing_ids = self.__class__.objects.order_by("id").values_list("id", flat=True)
                next_id = 1
                for existing_id in existing_ids:
                    if existing_id != next_id:
                        break
                    next_id += 1
                self.pk = next_id
                super().save(*args, **kwargs)
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
