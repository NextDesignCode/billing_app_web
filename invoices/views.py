from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from .utils import generate_invoice_pdf, generate_invoice_excel


class InvoiceListView(LoginRequiredMixin, ListView):
    """List all invoices with filtering and search"""
    model = Invoice
    template_name = 'invoices/list.html'
    context_object_name = 'invoices'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client')

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by client
        client_id = self.request.GET.get('client')
        if client_id:
            queryset = queryset.filter(client_id=client_id)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(client__name__icontains=search)
            )

        return queryset


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    """Display invoice details with items"""
    model = Invoice
    template_name = 'invoices/detail.html'
    context_object_name = 'invoice'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('product').all()
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    """Create a new invoice"""
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/create.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Facture {form.instance.invoice_number} créée avec succès!')
        return response

    def get_success_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.object.pk})


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing invoice"""
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/edit.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, 'Facture mise à jour!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.object.pk})


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an invoice"""
    model = Invoice
    template_name = 'invoices/confirm_delete.html'
    success_url = reverse_lazy('invoices:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        invoice_number = self.get_object().invoice_number
        messages.success(request, f'Facture {invoice_number} supprimée!')
        return super().delete(request, *args, **kwargs)


class InvoiceAddItemView(LoginRequiredMixin, CreateView):
    """Add an item to an invoice"""
    model = InvoiceItem
    form_class = InvoiceItemForm
    template_name = 'invoices/add_item.html'
    login_url = 'accounts:login'

    def dispatch(self, request, *args, **kwargs):
        self.invoice = get_object_or_404(Invoice, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        return context

    def form_valid(self, form):
        form.instance.invoice = self.invoice

        # Auto-fill description and price from product if selected
        if form.instance.product and not form.instance.description:
            form.instance.description = form.instance.product.name
        if form.instance.product and not form.instance.unit_price:
            form.instance.unit_price = form.instance.product.unit_price

        response = super().form_valid(form)
        messages.success(self.request, 'Article ajouté à la facture!')
        return response

    def get_success_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.invoice.pk})


class InvoiceExportPDFView(LoginRequiredMixin, View):
    """Export invoice as PDF"""
    login_url = 'accounts:login'

    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        pdf_buffer = generate_invoice_pdf(invoice)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{invoice.invoice_number}.pdf"'
        return response


class InvoiceExportExcelView(LoginRequiredMixin, View):
    """Export invoice as Excel"""
    login_url = 'accounts:login'

    def get(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        excel_buffer = generate_invoice_excel(invoice)

        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="facture_{invoice.invoice_number}.xlsx"'
        return response
