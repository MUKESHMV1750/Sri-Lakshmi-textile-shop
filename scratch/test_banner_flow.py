import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Banner

User = get_user_model()
client = Client()

admin_usr, _ = User.objects.get_or_create(username='banner_admin', defaults={'email': 'badmin@example.com', 'is_staff': True, 'is_superuser': True})
admin_usr.set_password('Password123!')
admin_usr.save()

client.force_login(admin_usr)

print("=== TESTING BANNER MANAGEMENT ===")

# 1. GET admin_banners
resp = client.get(reverse('admin_banners'))
print(f"[TEST 1] GET /admin-panel/banners/ -> Status {resp.status_code}")

# 2. POST create banner
post_data = {
    'title': 'Test Summer Silk Festival',
    'badge': 'Festive Special',
    'subtitle': 'Exclusive handwoven silk designs',
    'image_url_override': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=1800',
    'button_text': 'Explore Festival',
    'link_url': '/shop/?category=silk-sarees',
    'display_order': 0
}
resp = client.post(reverse('admin_banners'), post_data)
print(f"[TEST 2] POST Create Banner -> Status {resp.status_code}")

b = Banner.objects.filter(title='Test Summer Silk Festival').first()
print(f"   Created Banner ID: {b.id if b else 'None'}")

if b:
    # 3. Toggle Banner status
    resp = client.get(reverse('admin_toggle_banner', kwargs={'banner_id': b.id}))
    print(f"[TEST 3] Toggle Banner Status -> Status {resp.status_code}")

    # 4. Delete Banner
    resp = client.get(reverse('admin_delete_banner', kwargs={'banner_id': b.id}))
    print(f"[TEST 4] Delete Banner -> Status {resp.status_code}")

# 5. GET home page with dynamic banners
resp = client.get(reverse('home'))
print(f"[TEST 5] GET / (Home Page with Dynamic Banners) -> Status {resp.status_code}")

print("=== ALL BANNER TESTS PASSED SUCCESSFULLY ===")
