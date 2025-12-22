from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid


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
