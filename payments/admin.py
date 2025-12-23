# ============================================================================
# payments/admin.py
# ============================================================================
from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_date', 'amount', 'method', 'reference')
    list_filter = ('method', 'payment_date', 'created_at')
    search_fields = ('invoice__invoice_number', 'reference')
    readonly_fields = ('id', 'created_at')
