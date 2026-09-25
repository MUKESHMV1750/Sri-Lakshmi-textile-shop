from django.db import models
from django.conf import settings
from products.models import Product


class Review(models.Model):
    """Product reviews"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}★)"

    class Meta:
        db_table = 'reviews'
        unique_together = ['product', 'user']
        ordering = ['-created_at']
