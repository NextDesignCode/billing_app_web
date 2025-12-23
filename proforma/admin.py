# ============================================================================
# proforma/admin.py
# ============================================================================
from django.contrib import admin
from .models import ProformaInvoice, ProformaItem


class ProformaItemInline(admin.TabularInline):
    model = ProformaItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')


@admin.register(ProformaInvoice)
class ProformaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('proforma_number', 'client', 'issue_date', 'expiry_date', 'total', 'status')
    list_filter = ('status', 'issue_date', 'created_at')
    search_fields = ('proforma_number', 'client__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [ProformaItemInline]
