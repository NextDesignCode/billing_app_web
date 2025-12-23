from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid


class Product(models.Model):
    """Product/Article catalog"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('Product Name'))
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_('SKU'))
    reference = models.CharField(max_length=100, blank=True, db_index=True, verbose_name=_('Reference'))

    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name=_('Unit Price')
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name=_('Cost Price')
    )

    quantity_in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_level = models.IntegerField(default=10, validators=[MinValueValidator(0)],
                                        verbose_name=_('Reorder Level'))

    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=20,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name=_('Tax Rate (%)')
    )
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

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
