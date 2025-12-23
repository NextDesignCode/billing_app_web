# ============================================================================
# proforma/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'proforma'

urlpatterns = [
    path('', views.ProformaInvoiceListView.as_view(), name='list'),
    path('<uuid:pk>/', views.ProformaInvoiceDetailView.as_view(), name='detail'),
    path('create/', views.ProformaInvoiceCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.ProformaInvoiceUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.ProformaInvoiceDeleteView.as_view(), name='delete'),
]
