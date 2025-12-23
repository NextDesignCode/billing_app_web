# ============================================================================
# delivery/admin.py
# ============================================================================
from django.contrib import admin
from .models import DeliveryNote, DeliveryItem


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
