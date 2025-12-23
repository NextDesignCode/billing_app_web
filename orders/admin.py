# ============================================================================
# orders/admin.py
# ============================================================================
from django.contrib import admin
from .models import CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem


class CustomerOrderItemInline(admin.TabularInline):
    model = CustomerOrderItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client', 'order_date', 'delivery_date', 'total', 'status')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('order_number', 'client__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [CustomerOrderItemInline]


class SupplierOrderItemInline(admin.TabularInline):
    model = SupplierOrderItem
    extra = 1
    readonly_fields = ('subtotal', 'tax', 'total')


@admin.register(SupplierOrder)
class SupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_order_number', 'supplier', 'order_date', 'expected_delivery', 'total', 'status')
    list_filter = ('status', 'order_date', 'created_at')
    search_fields = ('purchase_order_number', 'supplier__name', 'description')
    readonly_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [SupplierOrderItemInline]
