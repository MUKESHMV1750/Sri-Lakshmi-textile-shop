from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart_post'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]
