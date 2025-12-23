# ============================================================================
# accounts/models.py
# ============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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
    language = models.CharField(max_length=10, default='fr',
                                choices=[('fr', 'Français'), ('en', 'English')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
