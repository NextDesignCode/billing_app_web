from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, URLValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid

# ============================================================================
# User & Authentication Models
# ============================================================================

class UserProfile(models.Model):
    """Extended user profile with roles and permissions"""
    
    ROLE_CHOICES = [
        ('admin', _('Administrator')),
        ('manager', _('Manager')),
        ('user', _('Standard User')),
        ('accountant', _('Accountant')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name=_('Tax ID'))
    language = models.CharField(max_length=10, default='fr', choices=[('fr', 'Français'), ('en', 'English')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"


# ============================================================================
# Client & Supplier Models
# ============================================================================

class Client(models.Model):
    """Client/Customer model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('Client Name'))
    company = models.CharField(max_length=255, blank=True, verbose_name=_('Company'))
    email = models.EmailField(blank=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name=_('Tax ID'))
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True, verbose_name=_('Payment Terms'))
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, 
                                       verbose_name=_('Credit Limit'), validators=[MinValueValidator(Decimal('0'))])
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name


class Supplier(models.Model):
    """Supplier/Vendor model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('Supplier Name'))
    company = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    address = models.TextField(verbose_name=_('Address'))
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name=_('Tax ID'))
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='suppliers_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name


# ============================================================================
# Product Model
# ============================================================================

class Product(models.Model):
    """Product/Article catalog"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('Product Name'))
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_('SKU'))
    reference = models.CharField(max_length=100, blank=True, db_index=True, verbose_name=_('Reference'))
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))],
                                     verbose_name=_('Unit Price'))
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                     validators=[MinValueValidator(Decimal('0'))], verbose_name=_('Cost Price'))
    
    # Stock Management
    quantity_in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(default=10, validators=[MinValueValidator(0)], verbose_name=_('Reorder Level'))
    
    # Tax & Category
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20, validators=[MinValueValidator(Decimal('0'))],
                                   verbose_name=_('Tax Rate (%)'))
    category = models.CharField(max_length=100, blank=True, db_index=True)
    unit = models.CharField(max_length=50, default='pcs', verbose_name=_('Unit of Measurement'))
    
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level


# ============================================================================
# Invoice & Related Documents Models
# ============================================================================

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


class ProformaInvoice(models.Model):
    """Proforma invoice (quotation)"""
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('sent', _('Sent')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proforma_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='proforma_invoices')
    
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


class ProformaItem(models.Model):
    """Line items for proforma invoice"""
    
    proforma = models.ForeignKey(ProformaInvoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
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


class DeliveryNote(models.Model):
    """Delivery note/Bon de livraison"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='delivery_notes')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_notes')
    
    delivery_date = models.DateField(db_index=True)
    expected_delivery = models.DateField(blank=True, null=True)
    actual_delivery = models.DateField(blank=True, null=True)
    
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='delivery_notes_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-delivery_date']
        verbose_name = _('Delivery Note')
        verbose_name_plural = _('Delivery Notes')
    
    def __str__(self):
        return f"Delivery {self.delivery_number}"


class DeliveryItem(models.Model):
    """Line items for delivery note"""
    
    delivery_note = models.ForeignKey(DeliveryNote, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_delivered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _('Delivery Item')
        verbose_name_plural = _('Delivery Items')


# ============================================================================
# Order Models
# ============================================================================

class CustomerOrder(models.Model):
    """Customer purchase order"""
    
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
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders')
    
    order_date = models.DateField(db_index=True)
    delivery_date = models.DateField(blank=True, null=True)
    
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


class CustomerOrderItem(models.Model):
    """Line items for customer order"""
    
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
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


class SupplierOrder(models.Model):
    """Purchase order from supplier"""
    
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
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    
    order_date = models.DateField(db_index=True)
    expected_delivery = models.DateField(blank=True, null=True)
    
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


class SupplierOrderItem(models.Model):
    """Line items for supplier order"""
    
    order = models.ForeignKey(SupplierOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
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


# ============================================================================
# Payment Model
# ============================================================================

class Payment(models.Model):
    """Payment tracking"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', _('Cash')),
        ('check', _('Check')),
        ('bank_transfer', _('Bank Transfer')),
        ('credit_card', _('Credit Card')),
        ('other', _('Other')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    
    payment_date = models.DateField(db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
    
    def __str__(self):
        return f"Payment for {self.invoice.invoice_number} - {self.amount}"


# ============================================================================
# Analytics & Reporting
# ============================================================================

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
