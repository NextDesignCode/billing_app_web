# ============================================================================
# core/utils.py - Utilitaires communs
# ============================================================================
from decimal import Decimal
from django.utils import timezone


def generate_next_number(model, field_name, prefix=''):
    """Generate next sequential number for invoices, orders, etc."""
    last_obj = model.objects.order_by('-created_at').first()

    if last_obj:
        last_number = getattr(last_obj, field_name)
        try:
            if prefix:
                num = int(last_number.replace(prefix, '').replace('-', ''))
            else:
                num = int(last_number)
            next_num = num + 1
        except:
            next_num = 1
    else:
        next_num = 1

    if prefix:
        return f"{prefix}{next_num:05d}"
    return str(next_num)


def format_currency(value, currency='€'):
    """Format decimal value as currency"""
    if isinstance(value, Decimal):
        return f"{value:,.2f} {currency}"
    return f"{float(value):,.2f} {currency}"


def get_date_range(period='month'):
    """Get start and end dates for a period"""
    today = timezone.now().date()

    if period == 'today':
        return today, today
    elif period == 'week':
        start = today - timezone.timedelta(days=today.weekday())
        return start, today
    elif period == 'month':
        start = today.replace(day=1)
        return start, today
    elif period == 'year':
        start = today.replace(month=1, day=1)
        return start, today

    return None, None
