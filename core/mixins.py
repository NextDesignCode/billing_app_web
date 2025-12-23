# ============================================================================
# core/mixins.py - Mixins réutilisables pour toutes les apps
# ============================================================================
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class FormMessageMixin:
    """Mixin pour ajouter des messages de succès automatiques"""
    success_message = None
    error_message = None

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class UserCreatedMixin:
    """Mixin pour auto-assigner created_by à l'utilisateur connecté"""

    def form_valid(self, form):
        if hasattr(form.instance, 'created_by') and not form.instance.created_by:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class OwnershipRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est le propriétaire"""

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or self.request.user.is_staff


class SearchMixin:
    """Mixin pour ajouter une fonctionnalité de recherche"""
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')

        if search and self.search_fields:
            from django.db.models import Q
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(query)

        return queryset


class ExportMixin:
    """Mixin pour ajouter des capacités d'export"""

    def get_export_filename(self):
        """Retourne le nom du fichier d'export"""
        return f"{self.model._meta.verbose_name_plural}_export"

    def export_pdf(self, queryset):
        """À implémenter dans les vues enfants"""
        raise NotImplementedError("Méthode export_pdf doit être implémentée")

    def export_excel(self, queryset):
        """À implémenter dans les vues enfants"""
        raise NotImplementedError("Méthode export_excel doit être implémentée")


class AuditMixin:
    """Mixin pour logger les actions importantes"""

    def form_valid(self, form):
        action = 'created' if not form.instance.pk else 'updated'
        response = super().form_valid(form)
        # Ici, vous pouvez logger l'action dans une table d'audit
        # AuditLog.objects.create(user=self.request.user, action=action, model=...)
        return response
