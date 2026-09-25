from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or 'category'
            slug = base_slug
            count = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']


class Product(models.Model):
    """Product model for the textile shop"""
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('Free', 'Free Size'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    fabric = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)
    available_sizes = models.JSONField(default=list, blank=True)
    available_colors = models.JSONField(default=list, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"LL-{uuid.uuid4().hex[:8].upper()}"
        if not self.slug:
            base_slug = slugify(self.name) or 'product'
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.sale_price and self.price > 0:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0

    @property
    def effective_price(self):
        return self.sale_price if self.sale_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(product=self, is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    @property
    def review_count(self):
        from reviews.models import Review
        return Review.objects.filter(product=self, is_approved=True).count()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']


class ProductImage(models.Model):
    """Product images - multiple per product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    @property
    def image_url(self):
        if self.image:
            url = str(self.image)
            if url.startswith('http://') or url.startswith('https://'):
                return url
            try:
                return self.image.url
            except Exception:
                return f"/media/{url}"
        return ''

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"

    class Meta:
        db_table = 'product_images'
        ordering = ['display_order']


class Coupon(models.Model):
    """Discount coupons"""
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(default=0)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active
            and self.valid_from <= now <= self.valid_until
            and (self.usage_limit == 0 or self.used_count < self.usage_limit)
        )

    class Meta:
        db_table = 'coupons'


class Banner(models.Model):
    """Hero Carousel Banner Model for Homepage"""
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    badge = models.CharField(max_length=100, blank=True, default='New Collection 2026')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    image_url_override = models.CharField(max_length=500, blank=True)
    link_url = models.CharField(max_length=200, default='/shop/')
    button_text = models.CharField(max_length=50, default='Shop Now')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.image_url_override:
            return self.image_url_override
        return "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80&w=1800"

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'banners'
        ordering = ['display_order', '-created_at']
