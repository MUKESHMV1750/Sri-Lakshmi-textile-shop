import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template.loader import get_template
from django.urls import get_resolver

print("--- STARTING SYSTEM AUDIT ---")

# 1. Audit URL resolver names
resolver = get_resolver()
url_names = set()

def get_urls(url_patterns, prefix=''):
    for pattern in url_patterns:
        if hasattr(pattern, 'url_patterns'):
            get_urls(pattern.url_patterns, prefix)
        elif hasattr(pattern, 'name') and pattern.name:
            url_names.add(pattern.name)

get_urls(resolver.url_patterns)
print(f"Total URL routes found: {len(url_names)}")

# 2. Audit template syntax & URL tag validity
template_dir = 'templates'
error_count = 0
templates_checked = 0

url_tag_pattern = re.compile(r"\{%\s*url\s+['\"]([\w_:-]+)['\"]")

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            templates_checked += 1
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, template_dir).replace('\\', '/')
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check template compilation
            try:
                get_template(rel_path)
            except Exception as e:
                print(f"[ERROR] TEMPLATE SYNTAX ERROR in {rel_path}: {e}")
                error_count += 1

            # Check url tags
            matches = url_tag_pattern.findall(content)
            for url_name in matches:
                if url_name not in url_names and not url_name.startswith('admin:'):
                    print(f"[WARN] BROKEN URL TAG '{url_name}' in {rel_path}")
                    error_count += 1

            # Check forms for missing csrf_token
            if '<form' in content and 'method="post"' in content.lower():
                if '{% csrf_token %}' not in content:
                    print(f"[WARN] MISSING CSRF TOKEN in POST form in {rel_path}")
                    error_count += 1

print(f"\nChecked {templates_checked} templates. Found {error_count} issues.")
