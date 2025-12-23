# ============================================================================
# payments/views.py
# ============================================================================
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm


class PaymentListView(LoginRequiredMixin, ListView):
    """List all payments"""
    model = Payment
    template_name = 'payments/list.html'
    context_object_name = 'payments'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('invoice', 'invoice__client')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(invoice__invoice_number__icontains=search) |
                Q(reference__icontains=search)
            )

        return queryset


class PaymentDetailView(LoginRequiredMixin, DetailView):
    """Display payment details"""
    model = Payment
    template_name = 'payments/detail.html'
    context_object_name = 'payment'
    login_url = 'accounts:login'


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Create a new payment"""
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/create.html'
    success_url = reverse_lazy('payments:list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Paiement de {form.instance.amount}€ enregistré!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unpaid or partially paid invoices
        from invoices.models import Invoice
        context['invoices'] = Invoice.objects.filter(
            status__in=['sent', 'partial']
        ).select_related('client').order_by('-invoice_date')
        return context


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a payment"""
    model = Payment
    template_name = 'payments/confirm_delete.html'
    success_url = reverse_lazy('payments:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        payment = self.get_object()
        amount = payment.amount
        messages.success(request, f'Paiement de {amount}€ supprimé!')
        return super().delete(request, *args, **kwargs)
