from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid


class CustomerOrder(models.Model):
    """Customer Order model"""

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('partial', _('Partially Delivered')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='orders')

    order_date = models.DateField(db_index=True)
    delivery_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer_orders_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']
        verbose_name = _('Customer Order')
        verbose_name_plural = _('Customer Orders')

    def __str__(self):
        return f"Order {self.order_number}"

    def get_absolute_url(self):
        return reverse('orders:customer_detail', kwargs={'pk': self.pk})

    def calculate_totals(self):
        """Recalculate order totals"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        self.tax_amount = sum(item.tax for item in items)
        self.total = self.subtotal + self.tax_amount
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = CustomerOrder.objects.order_by('-created_at').first()
            if last_order and last_order.order_number:
                try:
                    last_num = int(last_order.order_number.split('-')[-1])
                    self.order_number = f"CMD-{last_num + 1:05d}"
                except:
                    self.order_number = f"CMD-{CustomerOrder.objects.count() + 1:05d}"
            else:
                self.order_number = "CMD-00001"
        super().save(*args, **kwargs)


class CustomerOrderItem(models.Model):
    """Customer Order line items"""

    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    tax = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _('Customer Order Item')
        verbose_name_plural = _('Customer Order Items')

    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        self.tax = (self.subtotal * self.tax_rate / 100).quantize(Decimal('0.01'))
        self.total = (self.subtotal + self.tax).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        self.order.calculate_totals()

    def __str__(self):
        return f"{self.description} - {self.order.order_number}"


class SupplierOrder(models.Model):
    """Supplier Purchase Order model"""

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('confirmed', _('Confirmed')),
        ('partial', _('Partially Received')),
        ('received', _('Received')),
        ('cancelled', _('Cancelled')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order_number = models.CharField(max_length=100, unique=True, db_index=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, related_name='purchase_orders')

    order_date = models.DateField(db_index=True)
    expected_delivery = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supplier_orders_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']
        verbose_name = _('Supplier Order')
        verbose_name_plural = _('Supplier Orders')

    def __str__(self):
        return f"PO {self.purchase_order_number}"

    def get_absolute_url(self):
        return reverse('orders:supplier_detail', kwargs={'pk': self.pk})

    def calculate_totals(self):
        """Recalculate order totals"""
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        self.tax_amount = sum(item.tax for item in items)
        self.total = self.subtotal + self.tax_amount
        self.save()

    def save(self, *args, **kwargs):
        if not self.purchase_order_number:
            last_order = SupplierOrder.objects.order_by('-created_at').first()
            if last_order and last_order.purchase_order_number:
                try:
                    last_num = int(last_order.purchase_order_number.split('-')[-1])
                    self.purchase_order_number = f"PO-{last_num + 1:05d}"
                except:
                    self.purchase_order_number = f"PO-{SupplierOrder.objects.count() + 1:05d}"
            else:
                self.purchase_order_number = "PO-00001"
        super().save(*args, **kwargs)


class SupplierOrderItem(models.Model):
    """Supplier Order line items"""

    order = models.ForeignKey(SupplierOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    tax = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _('Supplier Order Item')
        verbose_name_plural = _('Supplier Order Items')

    def save(self, *args, **kwargs):
        self.subtotal = (self.quantity * self.unit_price).quantize(Decimal('0.01'))
        self.tax = (self.subtotal * self.tax_rate / 100).quantize(Decimal('0.01'))
        self.total = (self.subtotal + self.tax).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
        self.order.calculate_totals()

    def __str__(self):
        return f"{self.description} - {self.order.purchase_order_number}"
