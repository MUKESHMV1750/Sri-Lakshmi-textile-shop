import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
admin_usr, _ = User.objects.get_or_create(username='test_admin_user', defaults={'email': 'adminusr@example.com', 'is_staff': True, 'is_superuser': True})
admin_usr.set_password('AdminPass123!')
admin_usr.save()

client = Client()
client.force_login(admin_usr)

resp = client.get('/admin/', follow=True)
print(f"GET /admin/ as ADMIN -> Redirect chain: {resp.redirect_chain}, Status: {resp.status_code}")

resp2 = client.get('/admin-panel/', follow=True)
print(f"GET /admin-panel/ as ADMIN -> Redirect chain: {resp2.redirect_chain}, Status: {resp2.status_code}")
