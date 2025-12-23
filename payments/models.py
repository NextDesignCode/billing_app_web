# ============================================================================
# payments/models.py
# ============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid


class Payment(models.Model):
    """Payment model for invoice payments"""

    METHOD_CHOICES = [
        ('cash', _('Cash')),
        ('check', _('Check')),
        ('bank_transfer', _('Bank Transfer')),
        ('credit_card', _('Credit Card')),
        ('other', _('Other')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0'))])
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='bank_transfer')
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return f"Payment {self.amount} for {self.invoice.invoice_number}"

    def get_absolute_url(self):
        return reverse('payments:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice paid amount
        self.invoice.paid_amount = self.invoice.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0')

        # Update invoice status
        if self.invoice.paid_amount >= self.invoice.total:
            self.invoice.status = 'paid'
        elif self.invoice.paid_amount > 0:
            self.invoice.status = 'partial'

        self.invoice.save()
