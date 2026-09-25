from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """Shopping cart"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='user_cart')
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total(self):
        return self.subtotal

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.email}"
        return f"Cart - {self.session_key}"

    class Meta:
        db_table = 'cart'


class CartItem(models.Model):
    """Individual items in the cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=50, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.effective_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product', 'size', 'color']
