from django.urls import path
from . import views
from . import crud_views

app_name = 'core'

urlpatterns = [
    # Home & Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # ============ INVOICES ============
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<uuid:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/create/', crud_views.invoice_create, name='invoice_create'),
    path('invoices/<uuid:pk>/edit/', crud_views.invoice_edit, name='invoice_edit'),
    path('invoices/<uuid:pk>/delete/', crud_views.invoice_delete, name='invoice_delete'),
    path('invoices/<uuid:pk>/add-item/', crud_views.invoice_add_item, name='invoice_add_item'),
    path('invoices/<uuid:pk>/export-pdf/', crud_views.invoice_export_pdf, name='invoice_export_pdf'),
    path('invoices/<uuid:pk>/export-excel/', crud_views.invoice_export_excel, name='invoice_export_excel'),
    
    # ============ PROFORMA ============
    path('proforma/', crud_views.proforma_list, name='proforma_list'),
    path('proforma/<uuid:pk>/', crud_views.proforma_detail, name='proforma_detail'),
    path('proforma/create/', crud_views.proforma_create, name='proforma_create'),
    
    # ============ DELIVERY NOTES ============
    path('delivery/', crud_views.delivery_list, name='delivery_list'),
    path('delivery/<uuid:pk>/', crud_views.delivery_detail, name='delivery_detail'),
    path('delivery/create/', crud_views.delivery_create, name='delivery_create'),
    
    # ============ CUSTOMER ORDERS ============
    path('orders/customer/', crud_views.customer_order_list, name='customer_order_list'),
    path('orders/customer/<uuid:pk>/', crud_views.customer_order_detail, name='customer_order_detail'),
    path('orders/customer/create/', crud_views.customer_order_create, name='customer_order_create'),
    
    # ============ CLIENTS ============
    path('clients/', views.client_list, name='client_list'),
    path('clients/<uuid:pk>/', views.client_detail, name='client_detail'),
    path('clients/create/', crud_views.client_create, name='client_create'),
    path('clients/<uuid:pk>/edit/', crud_views.client_edit, name='client_edit'),
    path('clients/<uuid:pk>/delete/', crud_views.client_delete, name='client_delete'),
    
    # ============ PRODUCTS ============
    path('products/', views.product_list, name='product_list'),
    path('products/<uuid:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', crud_views.product_create, name='product_create'),
    path('products/<uuid:pk>/edit/', crud_views.product_edit, name='product_edit'),
    path('products/<uuid:pk>/delete/', crud_views.product_delete, name='product_delete'),
    
    # ============ PAYMENTS ============
    path('payments/', crud_views.payment_list, name='payment_list'),
    path('payments/create/', crud_views.payment_create, name='payment_create'),
    
    # ============ SUPPLIERS ============
    path('suppliers/', crud_views.supplier_list, name='supplier_list'),
    path('suppliers/create/', crud_views.supplier_create, name='supplier_create'),
    path('suppliers/<uuid:pk>/edit/', crud_views.supplier_edit, name='supplier_edit'),
    path('suppliers/<uuid:pk>/delete/', crud_views.supplier_delete, name='supplier_delete'),
    
    # ============ UTILITY ============
    path('search/', views.search, name='search'),
    path('reports/', views.reports, name='reports'),
]
