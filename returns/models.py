from django.db import models
from django.conf import settings
from orders.models import Order, OrderItem


class Return(models.Model):
    """Return and replacement requests"""
    RETURN_TYPE_CHOICES = [
        ('return', 'Return'),
        ('replacement', 'Replacement'),
        ('exchange', 'Exchange'),
    ]

    REASON_CHOICES = [
        ('damaged', 'Damaged Product'),
        ('wrong_item', 'Wrong Item Received'),
        ('size_issue', 'Size Issue'),
        ('color_issue', 'Color Mismatch'),
        ('quality_issue', 'Quality Issue'),
        ('not_as_described', 'Not as Described'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pickup_scheduled', 'Pickup Scheduled'),
        ('picked_up', 'Picked Up'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='returns')
    return_type = models.CharField(max_length=15, choices=RETURN_TYPE_CHOICES)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    admin_notes = models.TextField(blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return - {self.order.order_number} - {self.return_type}"

    class Meta:
        db_table = 'returns'
        ordering = ['-created_at']


class ReturnImage(models.Model):
    """Images uploaded for return requests"""
    return_request = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='returns/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'return_images'
