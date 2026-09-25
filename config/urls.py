from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home_view, about_view, contact_view

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('dashboard.urls')),
    path('dashboard/admin/', include('dashboard.urls')),
    path('admin-panel/', include('dashboard.urls')),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('shop/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('returns/', include('returns.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('reviews/', include('reviews.urls')),
    path('auth/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
