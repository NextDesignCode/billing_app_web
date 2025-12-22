from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users/profile', views.UserProfileViewSet, basename='userprofile')
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'products', views.ProductViewSet, basename='product')

router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', views.InvoiceItemViewSet, basename='invoiceitem')

router.register(r'proforma-invoices', views.ProformaInvoiceViewSet, basename='proformainvoice')
router.register(r'proforma-items', views.ProformaItemViewSet, basename='proformaitem')

router.register(r'delivery-notes', views.DeliveryNoteViewSet, basename='deliverynote')
router.register(r'delivery-items', views.DeliveryItemViewSet, basename='deliveryitem')

router.register(r'customer-orders', views.CustomerOrderViewSet, basename='customerorder')
router.register(r'customer-order-items', views.CustomerOrderItemViewSet, basename='customerorderitem')

router.register(r'supplier-orders', views.SupplierOrderViewSet, basename='supplierorder')
router.register(r'supplier-order-items', views.SupplierOrderItemViewSet, basename='supplierorderitem')

router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/overview/', views.dashboard_overview, name='dashboard-overview'),
    path('analytics/sales/', views.sales_statistics, name='sales-statistics'),
]
