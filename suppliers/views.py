# ============================================================================
# suppliers/models.py (already in suppliers/models.py - document 101)
# Keeping it here for reference
# ============================================================================

# ============================================================================
# suppliers/views.py
# ============================================================================
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Supplier
from .forms import SupplierForm


class SupplierListView(LoginRequiredMixin, ListView):
    """List all suppliers"""
    model = Supplier
    template_name = 'suppliers/list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search)
            )

        return queryset.order_by('name')


class SupplierDetailView(LoginRequiredMixin, DetailView):
    """Display supplier details"""
    model = Supplier
    template_name = 'suppliers/detail.html'
    context_object_name = 'supplier'
    login_url = 'accounts:login'


class SupplierCreateView(LoginRequiredMixin, CreateView):
    """Create a new supplier"""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/create.html'
    success_url = reverse_lazy('suppliers:list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Fournisseur {form.instance.name} créé!')
        return super().form_valid(form)


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing supplier"""
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/edit.html'
    success_url = reverse_lazy('suppliers:list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, f'Fournisseur {form.instance.name} mis à jour!')
        return super().form_valid(form)


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a supplier"""
    model = Supplier
    template_name = 'suppliers/confirm_delete.html'
    success_url = reverse_lazy('suppliers:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        supplier_name = self.get_object().name
        messages.success(request, f'Fournisseur {supplier_name} supprimé!')
        return super().delete(request, *args, **kwargs)
