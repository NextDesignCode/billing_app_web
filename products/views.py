from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.contrib import messages
from core.mixins import SearchMixin, UserCreatedMixin, FormMessageMixin
from .models import Product
from .forms import ProductForm


class ProductListView(LoginRequiredMixin, SearchMixin, ListView):
    """List all products with search and filtering"""
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20
    login_url = 'accounts:login'
    search_fields = ['name', 'sku', 'reference', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filter low stock
        if self.request.GET.get('low_stock'):
            queryset = queryset.filter(quantity_in_stock__lte=F('reorder_level'))

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.objects.values_list('category', flat=True).distinct()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Display product details"""
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    login_url = 'accounts:login'


class ProductCreateView(LoginRequiredMixin, UserCreatedMixin, FormMessageMixin, CreateView):
    """Create a new product"""
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('products:list')
    login_url = 'accounts:login'
    success_message = 'Produit créé avec succès!'


class ProductUpdateView(LoginRequiredMixin, FormMessageMixin, UpdateView):
    """Update an existing product"""
    model = Product
    form_class = ProductForm
    template_name = 'products/edit.html'
    success_url = reverse_lazy('products:list')
    login_url = 'accounts:login'
    success_message = 'Produit mis à jour!'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a product"""
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('products:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        product_name = self.get_object().name
        messages.success(request, f'Produit {product_name} supprimé!')
        return super().delete(request, *args, **kwargs)
