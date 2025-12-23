# ============================================================================
# delivery/urls.py
# ============================================================================
from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.DeliveryNoteListView.as_view(), name='list'),
    path('<uuid:pk>/', views.DeliveryNoteDetailView.as_view(), name='detail'),
    path('create/', views.DeliveryNoteCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.DeliveryNoteUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.DeliveryNoteDeleteView.as_view(), name='delete'),
]
