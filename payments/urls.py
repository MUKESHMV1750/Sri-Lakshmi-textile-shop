from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:order_id>/', views.payment_view, name='payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('success/<uuid:order_id>/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
