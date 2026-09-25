from django.test import TestCase
from products.models import Category, Product, Coupon

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Silk Sarees", slug="silk-sarees")
        self.product = Product.objects.create(
            name="Kanjeevaram Pure Silk",
            slug="kanjeevaram-pure-silk",
            category=self.category,
            description="Luxury Silk Saree",
            price=10000.00,
            sale_price=8000.00,
            sku="SKU-001",
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Kanjeevaram Pure Silk")
        self.assertEqual(self.product.discount_percentage, 20)
        self.assertEqual(self.product.effective_price, 8000.00)
        self.assertTrue(self.product.in_stock)

    def test_coupon_validity(self):
        from django.utils import timezone
        from datetime import timedelta
        coupon = Coupon.objects.create(
            code="TEST20",
            discount_type="percentage",
            discount_value=20.00,
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=10)
        )
        self.assertTrue(coupon.is_valid)
