# ============================================================================
# proforma/models.py
# ============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid


class ProformaInvoice(models.Model):
    """Proforma Invoice model"""

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proforma_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='proforma_invoices')

    issue_date = models.DateField(db_index=True)
    expiry_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='proforma_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = _('Proforma Invoice')
        verbose_name_plural = _('Proforma Invoices')

    def __str__(self):
        return f"Proforma {self.proforma_number}"

    def get_absolute_url(self):
        return reverse('proforma:detail', kwargs={'pk': self.pk})

    def calculate_totals(self):
        """Recalculate proforma totals"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        self.tax_amount = sum(item.tax for item in items)
        self.total = self.subtotal + self.tax_amount
        self.save()

    def save(self, *args, **kwargs):
        if not self.proforma_number:
            last_proforma = ProformaInvoice.objects.order_by('-created_at').first()
            if last_proforma and last_proforma.proforma_number:
                try:
                    last_num = int(last_proforma.proforma_number.split('-')[-1])
                    self.proforma_number = f"PRO-{last_num + 1:05d}"
                except:
                    self.proforma_number = f"PRO-{ProformaInvoice.objects.count() + 1:05d}"
            else:
                self.proforma_number = "PRO-00001"
        super().save(*args, **kwargs)


class ProformaItem(models.Model):
    """Proforma Invoice line items"""

    proforma = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    tax = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Proforma Item')
        verbose_name_plural = _('Proforma Items')

    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        self.tax = (self.subtotal * self.tax_rate / 100).quantize(Decimal('0.01'))
        self.total = (self.subtotal + self.tax).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        self.proforma.calculate_totals()

    def __str__(self):
        return f"{self.description} - {self.proforma.proforma_number}"
