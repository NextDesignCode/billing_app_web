# ============================================================================
# accounts/admin.py
# ============================================================================
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'role', 'company_name', 'language', 'created_at')
    list_filter = ('role', 'language', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'role', 'language')
        }),
        ('Entreprise', {
            'fields': ('company_name', 'tax_id')
        }),
        ('Contact', {
            'fields': ('phone', 'address', 'city', 'postal_code', 'country')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Utilisateur'
