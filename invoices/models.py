from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid

# Import des autres apps
from clients.models import Client
from products.models import Product


class Invoice(models.Model):
    """Standard invoice"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('paid', _('Paid')),
        ('partial', _('Partially Paid')),
        ('overdue', _('Overdue')),
        ('cancelled', _('Cancelled')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='invoices')
    
    # Dates
    invoice_date = models.DateField(db_index=True)
    due_date = models.DateField()
    
    # Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='invoices_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-invoice_date']
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['client']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
    def calculate_totals(self):
        """Recalculate invoice totals from line items"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.tax_amount = sum(item.tax for item in self.items.all())
        self.total = self.subtotal + self.tax_amount
        self.save()


class InvoiceItem(models.Model):
    """Line items for invoice"""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20, validators=[MinValueValidator(Decimal('0'))])
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    tax = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')
    
    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        self.tax = (self.subtotal * self.tax_rate / 100).quantize(Decimal('0.01'))
        self.total = (self.subtotal + self.tax).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.description} (Invoice {self.invoice.invoice_number})"
