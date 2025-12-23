from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'city', 'country')
    search_fields = ('name', 'company', 'email', 'phone', 'tax_id')
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Informations de base', {
            'fields': ('id', 'name', 'company', 'email', 'phone', 'fax')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'postal_code', 'country')
        }),
        ('Informations commerciales', {
            'fields': ('tax_id', 'payment_terms', 'credit_limit', 'website', 'contact_person')
        }),
        ('Statut', {
            'fields': ('is_active', 'notes')
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
