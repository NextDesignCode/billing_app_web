from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='list'),
    path('<uuid:pk>/', views.ClientDetailView.as_view(), name='detail'),
    path('create/', views.ClientCreateView.as_view(), name='create'),
    path('<uuid:pk>/edit/', views.ClientUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.ClientDeleteView.as_view(), name='delete'),
]
