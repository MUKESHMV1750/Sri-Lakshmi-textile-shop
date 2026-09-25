from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'phone', 'is_verified', 'date_joined']
    list_filter = ['is_verified', 'is_staff', 'gender']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'avatar', 'date_of_birth', 'gender', 'is_verified')}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'pincode', 'address_type', 'is_default']
    list_filter = ['address_type', 'state', 'is_default']
    search_fields = ['full_name', 'city', 'pincode']
