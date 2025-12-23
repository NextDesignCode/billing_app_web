# ============================================================================
# core/context_processors.py - Context processors globaux
#
# django context processors to add common data to all templates
from django.utils import timezone
def site_info(request):
    """Add site-wide information to all templates"""
    return {
        'site_name': 'Facturation Pro',
        'site_version': '2.0',
        'current_year': timezone.now().year,
    }


def user_notifications(request):
    """Add user notifications to context"""
    if not request.user.is_authenticated:
        return {}

    from invoices.models import Invoice
    from products.models import Product
    from django.db.models import F

    today = timezone.now().date()

    return {
        'overdue_invoices_count': Invoice.objects.filter(
            due_date__lt=today,
            status__in=['sent', 'partial']
        ).count(),
        'low_stock_count': Product.objects.filter(
            quantity_in_stock__lte=F('reorder_level')
        ).count(),
    }
