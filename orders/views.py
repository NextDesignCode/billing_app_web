# ============================================================================
# orders/views.py
# ============================================================================
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem
from .forms import CustomerOrderForm, SupplierOrderForm


# Customer Orders Views
class CustomerOrderListView(LoginRequiredMixin, ListView):
    """List all customer orders"""
    model = CustomerOrder
    template_name = 'orders/customer_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client')

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(client__name__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = CustomerOrder.STATUS_CHOICES
        return context


class CustomerOrderDetailView(LoginRequiredMixin, DetailView):
    """Display customer order details"""
    model = CustomerOrder
    template_name = 'orders/customer_detail.html'
    context_object_name = 'order'
    login_url = 'accounts:login'


class CustomerOrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new customer order"""
    model = CustomerOrder
    form_class = CustomerOrderForm
    template_name = 'orders/customer_create.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Commande {form.instance.order_number} créée!')
        return super().form_valid(form)


class CustomerOrderUpdateView(LoginRequiredMixin, UpdateView):
    """Update a customer order"""
    model = CustomerOrder
    form_class = CustomerOrderForm
    template_name = 'orders/customer_edit.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, 'Commande mise à jour!')
        return super().form_valid(form)


class CustomerOrderDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a customer order"""
    model = CustomerOrder
    template_name = 'orders/customer_confirm_delete.html'
    success_url = reverse_lazy('orders:customer_list')
    login_url = 'accounts:login'


# Supplier Orders Views
class SupplierOrderListView(LoginRequiredMixin, ListView):
    """List all supplier orders"""
    model = SupplierOrder
    template_name = 'orders/supplier_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('supplier')

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(purchase_order_number__icontains=search) |
                Q(supplier__name__icontains=search)
            )
        return queryset


class SupplierOrderDetailView(LoginRequiredMixin, DetailView):
    """Display supplier order details"""
    model = SupplierOrder
    template_name = 'orders/supplier_detail.html'
    context_object_name = 'order'
    login_url = 'accounts:login'


class SupplierOrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new supplier order"""
    model = SupplierOrder
    form_class = SupplierOrderForm
    template_name = 'orders/supplier_create.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Bon de commande {form.instance.purchase_order_number} créé!')
        return super().form_valid(form)


class SupplierOrderUpdateView(LoginRequiredMixin, UpdateView):
    """Update a supplier order"""
    model = SupplierOrder
    form_class = SupplierOrderForm
    template_name = 'orders/supplier_edit.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, 'Bon de commande mis à jour!')
        return super().form_valid(form)


class SupplierOrderDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a supplier order"""
    model = SupplierOrder
    template_name = 'orders/supplier_confirm_delete.html'
    success_url = reverse_lazy('orders:supplier_list')
    login_url = 'accounts:login'
