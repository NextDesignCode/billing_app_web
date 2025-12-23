from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='list'),
    path('<uuid:pk>/', views.InvoiceDetailView.as_view(), name='detail'),
    path('create/', views.InvoiceCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.InvoiceUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.InvoiceDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/add-item/', views.InvoiceAddItemView.as_view(), name='add_item'),
    path('<uuid:pk>/export-pdf/', views.InvoiceExportPDFView.as_view(), name='export_pdf'),
    path('<uuid:pk>/export-excel/', views.InvoiceExportExcelView.as_view(), name='export_excel'),
]
