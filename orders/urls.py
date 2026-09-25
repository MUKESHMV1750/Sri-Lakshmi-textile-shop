from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.order_list_view, name='order_list'),
    path('<uuid:order_id>/', views.order_detail_view, name='order_detail'),
    path('<uuid:order_id>/cancel/', views.cancel_order_view, name='cancel_order'),
]
