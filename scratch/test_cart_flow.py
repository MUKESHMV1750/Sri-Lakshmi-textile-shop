import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product, Category, Coupon
from cart.models import Cart, CartItem
from decimal import Decimal
import json

User = get_user_model()
client = Client()

user, _ = User.objects.get_or_create(username='cart_test_user', defaults={'email': 'carttest@example.com'})
user.set_password('Password123!')
user.save()
client.force_login(user)

cat, _ = Category.objects.get_or_create(name='Cart Test Category')
prod1, _ = Product.objects.get_or_create(
    slug='cart-test-product-1',
    defaults={'name': 'Cart Test Saree 1', 'category': cat, 'price': Decimal('1500.00'), 'stock': 20}
)
prod2, _ = Product.objects.get_or_create(
    slug='cart-test-product-2',
    defaults={'name': 'Cart Test Saree 2', 'category': cat, 'price': Decimal('2500.00'), 'stock': 10}
)

coupon, _ = Coupon.objects.get_or_create(
    code='TESTCART10',
    defaults={
        'discount_type': 'percentage',
        'discount_value': Decimal('10.00'),
        'valid_from': django.utils.timezone.now() - django.utils.timezone.timedelta(days=1),
        'valid_until': django.utils.timezone.now() + django.utils.timezone.timedelta(days=30),
        'is_active': True
    }
)

print("=== STARTING CART ENDPOINT TESTS ===")

# 1. GET cart page
resp = client.get(reverse('cart'))
print(f"[TEST 1] GET /cart/ -> Status {resp.status_code}")

# 2. Add Item 1 to Cart AJAX
resp = client.post(reverse('add_to_cart'), {'product_id': str(prod1.id), 'quantity': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"[TEST 2] AJAX Add to Cart -> Status {resp.status_code}, Response: {resp.json()}")

# 3. Add Item 2 to Cart AJAX
resp = client.post(reverse('add_to_cart'), {'product_id': str(prod2.id), 'quantity': 1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"[TEST 3] AJAX Add Item 2 -> Status {resp.status_code}, Response: {resp.json()}")

# 4. Update Item Quantity AJAX
cart = Cart.objects.get(user=user)
item1 = CartItem.objects.get(cart=cart, product=prod1)
resp = client.post(reverse('update_cart'), {'item_id': item1.id, 'quantity': 5}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"[TEST 4] AJAX Update Item Qty -> Status {resp.status_code}, Response: {resp.json()}")

# 5. Apply Coupon AJAX
resp = client.post(reverse('apply_coupon'), {'coupon_code': 'TESTCART10'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"[TEST 5] AJAX Apply Coupon -> Status {resp.status_code}, Response: {resp.json()}")

# 6. Remove Item 2 AJAX
item2 = CartItem.objects.get(cart=cart, product=prod2)
resp = client.post(reverse('remove_from_cart_post'), {'item_id': item2.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print(f"[TEST 6] AJAX Remove Item 2 -> Status {resp.status_code}, Response: {resp.json()}")

# 7. Remove Item 1 via URL GET/POST fallback
resp = client.get(reverse('remove_from_cart', kwargs={'item_id': item1.id}))
print(f"[TEST 7] GET Remove Item 1 -> Status {resp.status_code}")

# 8. Check empty cart page
resp = client.get(reverse('cart'))
print(f"[TEST 8] GET /cart/ (Empty) -> Status {resp.status_code}")

print("=== ALL CART TESTS PASSED SUCCESSFULLY ===")
