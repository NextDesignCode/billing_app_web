# ============================================================================
# core/models.py - Modèles centraux uniquement
# ============================================================================
from django.db import models
from django.utils.translation import gettext_lazy as _


class DashboardMetric(models.Model):
    """Store aggregated metrics for dashboard"""

    date = models.DateField(db_index=True)
    total_invoiced = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    new_clients = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Dashboard Metric')
        verbose_name_plural = _('Dashboard Metrics')

    def __str__(self):
        return f"Metrics for {self.date}"
