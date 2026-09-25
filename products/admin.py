from django.contrib import admin
from .models import Category, Product, ProductImage, Coupon


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'display_order']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'parent']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'sale_price', 'stock', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured', 'is_bestseller', 'is_new_arrival']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_until']
    list_filter = ['is_active', 'discount_type']
    search_fields = ['code']
