from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.admin_products, name='admin_products'),
    path('products/add/', views.admin_add_product, name='admin_add_product'),
    path('products/<uuid:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('products/<uuid:product_id>/delete/', views.admin_delete_product, name='admin_delete_product'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('orders/<uuid:order_id>/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('customers/', views.admin_customers, name='admin_customers'),
    path('returns/', views.admin_returns, name='admin_returns'),
    path('returns/<int:return_id>/update/', views.admin_update_return, name='admin_update_return'),
    path('coupons/', views.admin_coupons, name='admin_coupons'),
    path('reviews/', views.admin_reviews, name='admin_reviews'),
    path('reviews/<int:review_id>/toggle/', views.admin_toggle_review, name='admin_toggle_review'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('categories/<int:category_id>/delete/', views.admin_delete_category, name='admin_delete_category'),
    path('coupons/<int:coupon_id>/delete/', views.admin_delete_coupon, name='admin_delete_coupon'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/add/', views.admin_add_user, name='admin_add_user'),
    path('users/<int:user_id>/toggle-role/', views.admin_toggle_user_role, name='admin_toggle_user_role'),
    path('users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('banners/', views.admin_banners, name='admin_banners'),
    path('banners/<int:banner_id>/delete/', views.admin_delete_banner, name='admin_delete_banner'),
    path('banners/<int:banner_id>/toggle/', views.admin_toggle_banner, name='admin_toggle_banner'),
]
