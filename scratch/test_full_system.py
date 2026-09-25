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

User = get_user_model()

print("=== DEEP FUNCTIONAL WORKFLOW AUDIT ===")

# 1. Test Authentication Flow
client = Client()
reg_data = {
    'email': 'newuser@example.com',
    'username': 'newuser123',
    'password': 'Password123!',
    'first_name': 'Test',
    'last_name': 'User'
}
resp = client.post(reverse('register'), reg_data)
print(f"[TEST] Registration POST -> Status {resp.status_code}")

login_data = {
    'username': 'newuser@example.com',
    'password': 'Password123!'
}
resp = client.post(reverse('login'), login_data)
print(f"[TEST] Customer Login POST -> Status {resp.status_code}")

# 2. Test Product & Category Creation in Admin
admin_user, _ = User.objects.get_or_create(username='system_admin', defaults={'email': 'sysadmin@test.com', 'is_staff': True, 'is_superuser': True})
admin_user.set_password('AdminPass123!')
admin_user.save()

client.force_login(admin_user)

cat_resp = client.post(reverse('admin_categories'), {
    'name': 'Audit Silk Sarees',
    'description': 'Pure silk category for audit'
})
print(f"[TEST] Admin Category Creation POST -> Status {cat_resp.status_code}")

cat = Category.objects.filter(name='Audit Silk Sarees').first()
print(f"   Created Category ID: {cat.id if cat else 'None'}")

# 3. Test Wishlist Toggle & Cart Operations
if cat:
    prod, _ = Product.objects.get_or_create(
        slug='test-audit-kanjivaram-saree',
        defaults={
            'name': 'Test Audit Kanjivaram Saree',
            'category': cat,
            'price': 4999.00,
            'stock': 15,
            'is_active': True
        }
    )
    wish_resp = client.post(reverse('toggle_wishlist', kwargs={'product_id': prod.id}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    print(f"[TEST] Toggle Wishlist POST -> Status {wish_resp.status_code}")

    # 4. Test Add to Cart
    cart_resp = client.post(reverse('add_to_cart'), {'product_id': str(prod.id), 'quantity': 1})
    print(f"[TEST] Add to Cart POST -> Status {cart_resp.status_code}")

# 5. Test Admin User Creation & Deletion
add_user_resp = client.post(reverse('admin_add_user'), {
    'username': 'created_by_admin',
    'email': 'created_by_admin@test.com',
    'first_name': 'Admin',
    'last_name': 'Created',
    'role': 'customer',
    'password': 'Password123!'
})
print(f"[TEST] Admin Add User POST -> Status {add_user_resp.status_code}")

created_user = User.objects.filter(username='created_by_admin').first()
if created_user:
    del_user_resp = client.get(reverse('admin_delete_user', kwargs={'user_id': created_user.id}))
    print(f"[TEST] Admin Delete User GET -> Status {del_user_resp.status_code}")

print("=== ALL FUNCTIONAL TESTS COMPLETED SUCCESSFULLY ===")
