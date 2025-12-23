# ============================================================================
# proforma/views.py
# ============================================================================
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import ProformaInvoice, ProformaItem
from .forms import ProformaInvoiceForm, ProformaItemForm


class ProformaInvoiceListView(LoginRequiredMixin, ListView):
    """List all proforma invoices"""
    model = ProformaInvoice
    template_name = 'proforma/list.html'
    context_object_name = 'proformas'
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
                Q(proforma_number__icontains=search) |
                Q(client__name__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


class ProformaInvoiceDetailView(LoginRequiredMixin, DetailView):
    """Display proforma invoice details"""
    model = ProformaInvoice
    template_name = 'proforma/detail.html'
    context_object_name = 'proforma'
    login_url = 'accounts:login'


class ProformaInvoiceCreateView(LoginRequiredMixin, CreateView):
    """Create a new proforma invoice"""
    model = ProformaInvoice
    form_class = ProformaInvoiceForm
    template_name = 'proforma/create.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Proforma {form.instance.proforma_number} créée!')
        return super().form_valid(form)


class ProformaInvoiceUpdateView(LoginRequiredMixin, UpdateView):
    """Update a proforma invoice"""
    model = ProformaInvoice
    form_class = ProformaInvoiceForm
    template_name = 'proforma/edit.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, 'Proforma mise à jour!')
        return super().form_valid(form)


class ProformaInvoiceDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a proforma invoice"""
    model = ProformaInvoice
    template_name = 'proforma/confirm_delete.html'
    success_url = reverse_lazy('proforma:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        proforma_number = self.get_object().proforma_number
        messages.success(request, f'Proforma {proforma_number} supprimée!')
        return super().delete(request, *args, **kwargs)
