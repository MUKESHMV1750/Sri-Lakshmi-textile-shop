from django.urls import path
from . import views

urlpatterns = [
    path('', views.return_list, name='return_list'),
    path('request/<uuid:order_id>/', views.request_return, name='request_return'),
    path('status/<int:return_id>/', views.return_status, name='return_status'),
]
