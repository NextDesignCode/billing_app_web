# ============================================================================
# products/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<uuid:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.ProductUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.ProductDeleteView.as_view(), name='delete'),
]
