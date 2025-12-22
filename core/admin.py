from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    UserProfile, Client, Supplier, Product, Invoice, InvoiceItem,
    ProformaInvoice, ProformaItem, DeliveryNote, DeliveryItem,
    CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem,
    Payment, DashboardMetric
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'role', 'company_name', 'language')
    list_filter = ('role', 'language', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (_('User'), {'fields': ('user', 'role', 'language')}),
        (_('Company Info'), {'fields': ('company_name', 'tax_id')}),
        (_('Contact'), {'fields': ('phone', 'address', 'city', 'postal_code', 'country')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = _('User')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'city', 'country')
    search_fields = ('name', 'company', 'email', 'phone', 'tax_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Info'), {'fields': ('id', 'name', 'company', 'email', 'phone', 'fax')}),
        (_('Address'), {'fields': ('address', 'city', 'postal_code', 'country')}),
        (_('Business'), {'fields': ('tax_id', 'payment_terms', 'credit_limit', 'website', 'contact_person')}),
        (_('Status'), {'fields': ('is_active', 'notes')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'city', 'country')
    search_fields = ('name', 'company', 'email', 'phone', 'tax_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Basic Info'), {'fields': ('id', 'name', 'company', 'email', 'phone', 'fax')}),
        (_('Address'), {'fields': ('address', 'city', 'postal_code', 'country')}),
        (_('Business'), {'fields': ('tax_id', 'payment_terms', 'website', 'contact_person')}),
        (_('Status'), {'fields': ('is_active', 'notes')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'unit_price', 'quantity_in_stock', 'category', 'is_active')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'sku', 'reference', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Product Info'), {'fields': ('id', 'name', 'description', 'sku', 'reference')}),
        (_('Pricing'), {'fields': ('unit_price', 'cost_price', 'tax_rate')}),
        (_('Stock'), {'fields': ('quantity_in_stock', 'reorder_level')}),
        (_('Classification'), {'fields': ('category', 'unit')}),
        (_('Media'), {'fields': ('image',)}),
        (_('Status'), {'fields': ('is_active',)}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')
    fields = ('product', 'description', 'quantity', 'unit_price', 'tax_rate', 'subtotal', 'tax', 'total')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'invoice_date', 'due_date', 'total', 'status', 'paid_amount')
    list_filter = ('status', 'invoice_date', 'created_at')
    search_fields = ('invoice_number', 'client__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at', 'sent_at')
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        (_('Invoice Info'), {'fields': ('id', 'invoice_number', 'client', 'status')}),
        (_('Dates'), {'fields': ('invoice_date', 'due_date', 'sent_at')}),
        (_('Details'), {'fields': ('description', 'notes')}),
        (_('Totals'), {'fields': ('subtotal', 'tax_amount', 'total', 'paid_amount')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.calculate_totals()
        super().save_model(request, obj, form, change)


class ProformaItemInline(admin.TabularInline):
    model = ProformaItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')
    fields = ('product', 'description', 'quantity', 'unit_price', 'tax_rate', 'subtotal', 'tax', 'total')


@admin.register(ProformaInvoice)
class ProformaInvoiceAdmin(admin.ModelAdmin):
    list_display = ('proforma_number', 'client', 'issue_date', 'expiry_date', 'total', 'status')
    list_filter = ('status', 'issue_date', 'created_at')
    search_fields = ('proforma_number', 'client__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [ProformaItemInline]
    
    fieldsets = (
        (_('Proforma Info'), {'fields': ('id', 'proforma_number', 'client', 'status')}),
        (_('Dates'), {'fields': ('issue_date', 'expiry_date')}),
        (_('Details'), {'fields': ('description', 'notes')}),
        (_('Totals'), {'fields': ('subtotal', 'tax_amount', 'total')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1
    fields = ('product', 'description', 'quantity_ordered', 'quantity_delivered', 'unit_price')


@admin.register(DeliveryNote)
class DeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('delivery_number', 'client', 'delivery_date', 'actual_delivery')
    list_filter = ('delivery_date', 'created_at')
    search_fields = ('delivery_number', 'client__name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [DeliveryItemInline]
    
    fieldsets = (
        (_('Delivery Info'), {'fields': ('id', 'delivery_number', 'client', 'invoice')}),
        (_('Dates'), {'fields': ('delivery_date', 'expected_delivery', 'actual_delivery')}),
        (_('Details'), {'fields': ('description', 'notes')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


class CustomerOrderItemInline(admin.TabularInline):
    model = CustomerOrderItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')
    fields = ('product', 'description', 'quantity', 'unit_price', 'tax_rate', 'subtotal', 'tax', 'total')


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client', 'order_date', 'delivery_date', 'total', 'status')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('order_number', 'client__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [CustomerOrderItemInline]
    
    fieldsets = (
        (_('Order Info'), {'fields': ('id', 'order_number', 'client', 'status')}),
        (_('Dates'), {'fields': ('order_date', 'delivery_date')}),
        (_('Details'), {'fields': ('description', 'notes')}),
        (_('Totals'), {'fields': ('subtotal', 'tax_amount', 'total')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


class SupplierOrderItemInline(admin.TabularInline):
    model = SupplierOrderItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')
    fields = ('product', 'description', 'quantity', 'unit_price', 'quantity_received', 'tax_rate', 'subtotal', 'tax', 'total')


@admin.register(SupplierOrder)
class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_order_number', 'supplier', 'order_date', 'expected_delivery', 'total', 'status')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('purchase_order_number', 'supplier__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [SupplierOrderItemInline]
    
    fieldsets = (
        (_('Order Info'), {'fields': ('id', 'purchase_order_number', 'supplier', 'status')}),
        (_('Dates'), {'fields': ('order_date', 'expected_delivery')}),
        (_('Details'), {'fields': ('description', 'notes')}),
        (_('Totals'), {'fields': ('subtotal', 'tax_amount', 'total')}),
        (_('Audit'), {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_date', 'amount', 'method', 'reference')
    list_filter = ('method', 'payment_date', 'created_at')
    search_fields = ('invoice__invoice_number', 'reference')
    readonly_fields = ('id', 'created_at')
    
    fieldsets = (
        (_('Payment Info'), {'fields': ('id', 'invoice', 'payment_date', 'amount', 'method')}),
        (_('Details'), {'fields': ('reference', 'notes')}),
        (_('Audit'), {'fields': ('created_by', 'created_at'), 'classes': ('collapse',)}),
    )


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_invoiced', 'total_paid', 'total_orders', 'new_clients')
    list_filter = ('date',)
    readonly_fields = ('date', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Date'), {'fields': ('date',)}),
        (_('Metrics'), {'fields': ('total_invoiced', 'total_paid', 'total_orders', 'new_clients')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
