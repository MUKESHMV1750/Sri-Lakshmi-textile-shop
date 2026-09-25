import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product, Category
from cart.models import Cart, CartItem
from orders.models import Order
from wishlist.models import Wishlist
from reviews.models import Review
from accounts.models import Address

User = get_user_model()
client = Client()

user, _ = User.objects.get_or_create(username='audit_user_full', defaults={'email': 'fullaudit@example.com'})
user.set_password('pass1234')
user.save()
client.force_login(user)

cat, _ = Category.objects.get_or_create(name='Audit Category')
prod, _ = Product.objects.get_or_create(
    slug='audit-product-sample',
    defaults={'name': 'Audit Product Sample', 'category': cat, 'price': 1000, 'stock': 10}
)
cart = Cart.objects.get_or_create(user=user)[0]
CartItem.objects.get_or_create(cart=cart, product=prod, defaults={'quantity': 1})

addr, _ = Address.objects.get_or_create(
    user=user,
    defaults={
        'full_name': 'Audit User',
        'phone': '9876543210',
        'address_line_1': '123 Test St',
        'city': 'Chennai',
        'state': 'TN',
        'pincode': '600001'
    }
)

order, _ = Order.objects.get_or_create(
    order_number='ORD-AUDIT-100',
    defaults={
        'user': user,
        'address': addr,
        'subtotal': 1000,
        'total': 1000,
    }
)

review, _ = Review.objects.get_or_create(
    user=user,
    product=prod,
    defaults={'rating': 5, 'comment': 'Great product!'}
)

endpoints = [
    ('product_detail', {'slug': prod.slug}),
    ('order_detail', {'order_id': order.id}),
    ('cancel_order', {'order_id': order.id}),
    ('add_review', {'product_id': prod.id}),
    ('delete_review', {'review_id': review.id}),
]

print("=== CHECKING PARAMETERIZED VIEWS ===")
for name, kwargs in endpoints:
    try:
        url = reverse(name, kwargs=kwargs)
        resp = client.get(url)
        print(f"[OK] GET {name} ({url}) -> Status {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Exception on {name}: {e}")

print("=== DEEP AUDIT COMPLETED ===")
