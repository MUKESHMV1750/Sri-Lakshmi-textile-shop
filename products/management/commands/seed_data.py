import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage, Coupon
from reviews.models import Review

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds initial demo data for LoomLuxe textile shop'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data for LoomLuxe...'))

        # Create Admin User
        admin_email = 'admin@loomluxe.com'
        if not User.objects.filter(email=admin_email).exists():
            admin = User.objects.create_superuser(
                email=admin_email,
                username='admin',
                password='admin123',
                first_name='LoomLuxe',
                last_name='Admin',
                phone='+91 98765 43210',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin@loomluxe.com / admin123'))
        else:
            self.stdout.write('Superuser already exists.')

        # Create Customer Demo User
        demo_email = 'demo@example.com'
        if not User.objects.filter(email=demo_email).exists():
            demo_user = User.objects.create_user(
                email=demo_email,
                username='demouser',
                password='password123',
                first_name='Priya',
                last_name='Sharma',
                phone='+91 91234 56789'
            )
            self.stdout.write(self.style.SUCCESS('Demo user created: demo@example.com / password123'))
        else:
            demo_user = User.objects.get(email=demo_email)

        # Categories Data
        categories_data = [
            {'name': 'Silk Sarees', 'slug': 'silk-sarees', 'description': 'Handcrafted Pure Kanjeevaram & Banarasi Silk Sarees', 'display_order': 1},
            {'name': 'Cotton Fabrics', 'slug': 'cotton-fabrics', 'description': 'Breathable Organic & Handloom Cotton Textiles', 'display_order': 2},
            {'name': 'Designer Kurtis', 'slug': 'designer-kurtis', 'description': 'Contemporary & Ethnic Designer Kurti Collections', 'display_order': 3},
            {'name': 'Linen Fabrics', 'slug': 'linen-fabrics', 'description': 'Premium European Linen Textiles & Apparel', 'display_order': 4},
            {'name': 'Artisan Dupattas', 'slug': 'artisan-dupattas', 'description': 'Hand-painted & Embroidered Silk & Chiffon Dupattas', 'display_order': 5},
            {'name': 'Velvet & Embroidered', 'slug': 'velvet-embroidered', 'description': 'Luxury Royal Velvet & Heavy Zari Embroidery Fabrics', 'display_order': 6},
        ]

        cat_objs = {}
        for cat in categories_data:
            c, created = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults=cat
            )
            cat_objs[cat['slug']] = c

        # Sample Products Data
        products_data = [
            {
                'name': 'Royal Kanjeevaram Crimson Pure Silk Saree',
                'slug': 'royal-kanjeevaram-crimson-pure-silk-saree',
                'category': cat_objs['silk-sarees'],
                'description': 'Handwoven pure Kanjeevaram mulberry silk saree featuring intricate gold zari peacock motifs, solid woven border, and unstitched matching blouse piece. Crafted by master artisans in Tamil Nadu.',
                'short_description': 'Authentic Kanjeevaram silk saree with rich pure gold zari pallu.',
                'price': 24999.00,
                'sale_price': 19999.00,
                'sku': 'LL-SLK-001',
                'stock': 12,
                'fabric': 'Pure Kanjeevaram Silk',
                'color': 'Crimson Red',
                'available_sizes': ['Free'],
                'available_colors': ['Crimson Red', 'Royal Gold', 'Emerald Green'],
                'brand': 'LoomLuxe Heritage',
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'tags': ['silk', 'kanjeevaram', 'wedding', 'festive'],
                'img_url': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Banarasi Brocade Emerald Silk Dupatta',
                'slug': 'banarasi-brocade-emerald-silk-dupatta',
                'category': cat_objs['artisan-dupattas'],
                'description': 'Lustrous emerald green Banarasi silk dupatta enriched with ornate kadwa weave flora in fine metallic gold yarn. Elegant tassel trims on edges.',
                'short_description': 'Traditional Banarasi weave silk dupatta with rich zari border.',
                'price': 6999.00,
                'sale_price': 5499.00,
                'sku': 'LL-DUP-002',
                'stock': 25,
                'fabric': 'Banarasi Silk',
                'color': 'Emerald Green',
                'available_sizes': ['Free'],
                'available_colors': ['Emerald Green', 'Maroon', 'Deep Navy'],
                'brand': 'LoomLuxe Heritage',
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': True,
                'tags': ['dupatta', 'banarasi', 'festive'],
                'img_url': 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Handblock Ajrakh Print Organic Cotton Fabric (Per Meter)',
                'slug': 'handblock-ajrakh-print-organic-cotton-fabric',
                'category': cat_objs['cotton-fabrics'],
                'description': 'Pure 100% breathable organic cotton material hand-printed using ancient natural vegetable dyes and traditional wood block carving techniques.',
                'short_description': 'Pure organic cotton fabric with authentic handblock Ajrakh prints.',
                'price': 850.00,
                'sale_price': 699.00,
                'sku': 'LL-COT-003',
                'stock': 150,
                'fabric': '100% Handloom Cotton',
                'color': 'Indigo & Madder Red',
                'available_sizes': ['M', 'L'],
                'available_colors': ['Indigo Navy', 'Earth Rust', 'Olive Green'],
                'brand': 'LoomLuxe Organic',
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'tags': ['cotton', 'ajrakh', 'handblock', 'unstitched'],
                'img_url': 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Ivory Embroidered Chanderi Kurti Set',
                'slug': 'ivory-embroidered-chanderi-kurti-set',
                'category': cat_objs['designer-kurtis'],
                'description': 'Sophisticated ivory Chanderi tunic set styled with subtle thread embroidery, mirror accents, matching straight pants, and lightweight chiffon scarf.',
                'short_description': 'Elegant 3-piece Chanderi silk blend kurti set with floral embroidery.',
                'price': 8999.00,
                'sale_price': 7499.00,
                'sku': 'LL-KRT-004',
                'stock': 18,
                'fabric': 'Chanderi Silk Blend',
                'color': 'Ivory Gold',
                'available_sizes': ['S', 'M', 'L', 'XL'],
                'available_colors': ['Ivory Gold', 'Soft Blush', 'Sky Blue'],
                'brand': 'LoomLuxe Modern',
                'is_featured': False,
                'is_bestseller': True,
                'is_new_arrival': True,
                'tags': ['kurti', 'chanderi', 'partywear'],
                'img_url': 'https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Pastel French Linen Plain Weave Fabric',
                'slug': 'pastel-french-linen-plain-weave-fabric',
                'category': cat_objs['linen-fabrics'],
                'description': 'Sublime 100% pure French flax linen fabric. Pre-washed for superior softness, durability, and natural temperature regulation.',
                'short_description': 'Premium European pure flax linen fabric for shirts and dresses.',
                'price': 1499.00,
                'sale_price': None,
                'sku': 'LL-LIN-005',
                'stock': 80,
                'fabric': '100% French Flax Linen',
                'color': 'Sage Green',
                'available_sizes': ['Free'],
                'available_colors': ['Sage Green', 'Dusty Rose', 'Sand Beige', 'Natural White'],
                'brand': 'LoomLuxe Studio',
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': True,
                'tags': ['linen', 'casual', 'sustainable'],
                'img_url': 'https://images.unsplash.com/photo-1603252109303-2751441dd157?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Royal Midnight Velvet Zari Embroidered Anarkali Fabric',
                'slug': 'royal-midnight-velvet-zari-embroidered-fabric',
                'category': cat_objs['velvet-embroidered'],
                'description': 'Ultra-plush deep midnight blue micro velvet embellished with heavy antique gold zari thread work, dabka, and sequin highlights.',
                'short_description': 'Heavy zardozi embroidered luxury micro velvet fabric.',
                'price': 18999.00,
                'sale_price': 14999.00,
                'sku': 'LL-VLV-006',
                'stock': 10,
                'fabric': 'Micro Velvet',
                'color': 'Midnight Navy',
                'available_sizes': ['Free'],
                'available_colors': ['Midnight Navy', 'Deep Wine', 'Royal Emerald'],
                'brand': 'LoomLuxe Royal',
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': False,
                'tags': ['velvet', 'zari', 'bridal', 'lehenga'],
                'img_url': 'https://images.unsplash.com/photo-1544441893-675973e31985?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Chanderi Tissue Gold Silk Saree',
                'slug': 'chanderi-tissue-gold-silk-saree',
                'category': cat_objs['silk-sarees'],
                'description': 'Lightweight shimmer tissue Chanderi silk saree with subtle woven floral bootis and delicate scalloped borders.',
                'short_description': 'Glimmering Chanderi tissue silk saree with intricate scallop trim.',
                'price': 15999.00,
                'sale_price': 12999.00,
                'sku': 'LL-SLK-007',
                'stock': 14,
                'fabric': 'Chanderi Tissue Silk',
                'color': 'Champagne Gold',
                'available_sizes': ['Free'],
                'available_colors': ['Champagne Gold', 'Rose Gold'],
                'brand': 'LoomLuxe Heritage',
                'is_featured': False,
                'is_bestseller': True,
                'is_new_arrival': True,
                'tags': ['saree', 'chanderi', 'gold'],
                'img_url': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&auto=format&fit=crop'
            },
            {
                'name': 'Handwoven Tussar Silk Floral Dupatta',
                'slug': 'handwoven-tussar-silk-floral-dupatta',
                'category': cat_objs['artisan-dupattas'],
                'description': 'Textured natural wild Tussar silk dupatta featuring hand-painted Kalamkari motifs and gold tissue border.',
                'short_description': 'Authentic textured Tussar silk dupatta with Kalamkari floral design.',
                'price': 5299.00,
                'sale_price': 4499.00,
                'sku': 'LL-DUP-008',
                'stock': 20,
                'fabric': 'Wild Tussar Silk',
                'color': 'Natural Mustard',
                'available_sizes': ['Free'],
                'available_colors': ['Natural Mustard', 'Terracotta'],
                'brand': 'LoomLuxe Heritage',
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': False,
                'tags': ['tussar', 'kalamkari', 'artisan'],
                'img_url': 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&auto=format&fit=crop'
            }
        ]

        for pdata in products_data:
            img_url = pdata.pop('img_url')
            prod, created = Product.objects.get_or_create(
                sku=pdata['sku'],
                defaults=pdata
            )
            if created or not prod.images.exists():
                # We can store sample image URL reference or place an image record
                ProductImage.objects.create(
                    product=prod,
                    image=img_url,
                    alt_text=prod.name,
                    is_primary=True,
                    display_order=1
                )
                self.stdout.write(f'Created product: {prod.name}')

                # Create sample reviews
                Review.objects.create(
                    product=prod,
                    user=demo_user,
                    rating=5,
                    title='Absolute Masterpiece!',
                    comment='The texture, color intensity, and feel of this fabric surpassed my expectations. Delivery was very prompt as well.',
                    is_approved=True
                )

        # Coupons
        now = timezone.now()
        coupons = [
            {
                'code': 'WELCOME10',
                'description': '10% Off Your First Purchase',
                'discount_type': 'percentage',
                'discount_value': 10.00,
                'minimum_order': 1000.00,
                'maximum_discount': 2000.00,
                'usage_limit': 100,
                'valid_from': now - timedelta(days=1),
                'valid_until': now + timedelta(days=365)
            },
            {
                'code': 'LOOM20',
                'description': 'Flat ₹500 Off on orders above ₹3000',
                'discount_type': 'fixed',
                'discount_value': 500.00,
                'minimum_order': 3000.00,
                'usage_limit': 500,
                'valid_from': now - timedelta(days=1),
                'valid_until': now + timedelta(days=180)
            },
            {
                'code': 'SILK25',
                'description': '25% Special Festive Discount',
                'discount_type': 'percentage',
                'discount_value': 25.00,
                'minimum_order': 5000.00,
                'maximum_discount': 5000.00,
                'usage_limit': 50,
                'valid_from': now - timedelta(days=1),
                'valid_until': now + timedelta(days=90)
            }
        ]

        for cdata in coupons:
            Coupon.objects.get_or_create(code=cdata['code'], defaults=cdata)
            self.stdout.write(f"Coupon ready: {cdata['code']}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded LoomLuxe database!'))
