# ============================================================================
# payments/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('<uuid:pk>/', views.PaymentDetailView.as_view(), name='detail'),
    path('create/', views.PaymentCreateView.as_view(), name='create'),
    path('<uuid:pk>/delete/', views.PaymentDeleteView.as_view(), name='delete'),
]
