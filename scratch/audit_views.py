import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

print("--- AUDITING VIEWS & RESPONSES ---")

# Create a test user if not exists or get superuser
user, created = User.objects.get_or_create(username='test_audit_admin', defaults={
    'email': 'admin@test.com',
    'is_staff': True,
    'is_superuser': True
})
if created:
    user.set_password('pass1234')
    user.save()

client = Client()
client.force_login(user)

routes_to_test = [
    ('home', {}),
    ('shop', {}),
    ('cart', {}),
    ('checkout', {}),
    ('wishlist', {}),
    ('addresses', {}),
    ('order_list', {}),
    ('return_list', {}),
    ('my_account', {}),
    ('login', {}),
    ('register', {}),
    ('admin_dashboard', {}),
    ('admin_products', {}),
    ('admin_categories', {}),
    ('admin_orders', {}),
    ('admin_users', {}),
    ('admin_coupons', {}),
    ('admin_customers', {}),
    ('admin_reviews', {}),
    ('admin_returns', {}),
]

success_count = 0
fail_count = 0

for url_name, kwargs in routes_to_test:
    try:
        url = reverse(url_name, kwargs=kwargs)
        response = client.get(url)
        if response.status_code in [200, 302]:
            print(f"[OK] GET {url_name} ({url}) -> Status {response.status_code}")
            success_count += 1
        else:
            print(f"[FAIL] GET {url_name} ({url}) -> Status {response.status_code}")
            fail_count += 1
    except Exception as e:
        print(f"[ERROR] Exception on GET {url_name}: {e}")
        fail_count += 1

print(f"\nTested {len(routes_to_test)} main views. Success: {success_count}, Failures: {fail_count}")
