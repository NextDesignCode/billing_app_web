# ============================================================================
# invoice_project/urls.py - UPDATED with all modules
# ============================================================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Main app routes (dashboard, reports, etc.)
    path('', include('core.urls')),

    # Individual module routes
    path('clients/', include('clients.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('products/', include('products.urls')),
    path('invoices/', include('invoices.urls')),
    path('proforma/', include('proforma.urls')),
    path('delivery/', include('delivery.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),

    # API routes
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
