from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid


class DeliveryNote(models.Model):
    """Delivery Note model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery_number = models.CharField(max_length=100, unique=True, db_index=True)
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='delivery_notes')
    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_notes')

    delivery_date = models.DateField(db_index=True)
    expected_delivery = models.DateField(null=True, blank=True)
    actual_delivery = models.DateField(null=True, blank=True)

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

    def get_absolute_url(self):
        return reverse('delivery:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.delivery_number:
            last_delivery = DeliveryNote.objects.order_by('-created_at').first()
            if last_delivery and last_delivery.delivery_number:
                try:
                    last_num = int(last_delivery.delivery_number.split('-')[-1])
                    self.delivery_number = f"BL-{last_num + 1:05d}"
                except:
                    self.delivery_number = f"BL-{DeliveryNote.objects.count() + 1:05d}"
            else:
                self.delivery_number = "BL-00001"
        super().save(*args, **kwargs)


class DeliveryItem(models.Model):
    """Delivery Note line items"""

    delivery_note = models.ForeignKey(DeliveryNote, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_delivered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Delivery Item')
        verbose_name_plural = _('Delivery Items')

    def __str__(self):
        return f"{self.description} - {self.delivery_note.delivery_number}"
