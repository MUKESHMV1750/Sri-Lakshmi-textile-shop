from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('search/', views.search_suggestions, name='search_suggestions'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
]
