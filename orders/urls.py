# ============================================================================
# orders/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Customer Orders
    path('customer/', views.CustomerOrderListView.as_view(), name='customer_list'),
    path('customer/<uuid:pk>/', views.CustomerOrderDetailView.as_view(), name='customer_detail'),
    path('customer/create/', views.CustomerOrderCreateView.as_view(), name='customer_create'),
    path('customer/<uuid:pk>/edit/', views.CustomerOrderUpdateView.as_view(), name='customer_edit'),
    path('customer/<uuid:pk>/delete/', views.CustomerOrderDeleteView.as_view(), name='customer_delete'),

    # Supplier Orders
    path('supplier/', views.SupplierOrderListView.as_view(), name='supplier_list'),
    path('supplier/<uuid:pk>/', views.SupplierOrderDetailView.as_view(), name='supplier_detail'),
    path('supplier/create/', views.SupplierOrderCreateView.as_view(), name='supplier_create'),
    path('supplier/<uuid:pk>/edit/', views.SupplierOrderUpdateView.as_view(), name='supplier_edit'),
    path('supplier/<uuid:pk>/delete/', views.SupplierOrderDeleteView.as_view(), name='supplier_delete'),
]
