from django.contrib import admin
from .models import DashboardMetric


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_invoiced', 'total_paid', 'total_orders', 'new_clients')
    list_filter = ('date',)
    readonly_fields = ('date', 'created_at', 'updated_at')
