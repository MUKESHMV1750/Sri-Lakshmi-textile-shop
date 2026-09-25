from django.db import models
from django.conf import settings
from products.models import Product


class Wishlist(models.Model):
    """User wishlist"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"

    class Meta:
        db_table = 'wishlist'
        unique_together = ['user', 'product']
        ordering = ['-added_at']
