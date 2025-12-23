# ============================================================================
# core/views.py - Vues centrales (Dashboard, Reports)
# ============================================================================
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard with KPIs and recent activity"""
    template_name = 'dashboard.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Import models here to avoid circular imports
        from invoices.models import Invoice
        from clients.models import Client
        from suppliers.models import Supplier
        from products.models import Product
        from payments.models import Payment
        from orders.models import CustomerOrder, SupplierOrder

        # Invoice metrics
        context['total_invoiced'] = Invoice.objects.filter(
            status__in=['sent', 'paid']
        ).aggregate(total=Sum('total'))['total'] or 0

        context['total_paid'] = Invoice.objects.filter(
            status='paid'
        ).aggregate(total=Sum('total'))['total'] or 0

        context['pending_count'] = Invoice.objects.filter(status='sent').count()

        context['overdue_count'] = Invoice.objects.filter(
            status__in=['sent', 'partial'],
            due_date__lt=today
        ).count()

        # Client & Supplier metrics
        context['total_clients'] = Client.objects.filter(is_active=True).count()
        context['total_suppliers'] = Supplier.objects.filter(is_active=True).count()

        # Product metrics
        context['total_products'] = Product.objects.count()
        context['low_stock_products'] = Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        ).count()

        # Orders metrics
        context['pending_orders'] = CustomerOrder.objects.filter(status='pending').count()
        context['pending_supplier_orders'] = SupplierOrder.objects.filter(status='pending').count()

        # Recent data
        context['recent_invoices'] = Invoice.objects.select_related('client').order_by('-created_at')[:5]
        context['recent_payments'] = Payment.objects.select_related('invoice').order_by('-created_at')[:5]
        context['low_stock_items'] = Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        )[:5]

        # User profile
        if hasattr(self.request.user, 'userprofile'):
            context['user_profile'] = self.request.user.userprofile

        return context


class ReportsView(LoginRequiredMixin, TemplateView):
    """Reports and statistics page"""
    template_name = 'reports.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)

        from invoices.models import Invoice
        from clients.models import Client

        # Monthly metrics
        context['monthly_revenue'] = Invoice.objects.filter(
            created_at__gte=month_ago,
            status='paid'
        ).aggregate(total=Sum('total'))['total'] or 0

        context['monthly_invoices'] = Invoice.objects.filter(
            created_at__gte=month_ago
        ).count()

        context['monthly_clients'] = Client.objects.filter(
            created_at__gte=month_ago
        ).count()

        return context
