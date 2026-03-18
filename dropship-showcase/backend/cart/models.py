from django.db import models
from django.conf import settings


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_items"
        unique_together = [("user", "product_id")]
        ordering = ["created_at"]

    def __str__(self):
        return f"CartItem(user={self.user_id}, product={self.product_id}, qty={self.quantity})"
