from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.contrib import messages
from .models import Client
from .forms import ClientForm


class ClientListView(LoginRequiredMixin, ListView):
    """List all active clients with search functionality"""
    model = Client
    template_name = 'clients/list.html'
    context_object_name = 'clients'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by active status
        if not self.request.GET.get('show_inactive'):
            queryset = queryset.filter(is_active=True)

        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(tax_id__icontains=search) |
                Q(company__icontains=search)
            )

        return queryset.order_by('name')


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Display client details with related invoices"""
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Récupérer TOUTES les factures pour calculer les stats globales
        all_invoices = self.object.invoices.all()

        # 2. Récupérer SEULEMENT les 10 dernières pour l'affichage dans le tableau
        # On utilise .order_by() ici pour s'assurer que le slice prend les bonnes
        recent_invoices = all_invoices.order_by('-created_at')[:10]

        context['invoices'] = recent_invoices

        # 3. Calculer les statistiques sur le QuerySet complet (all_invoices)
        # et non pas sur le slice (recent_invoices)
        context['stats'] = {
            'total_invoiced': all_invoices.aggregate(total=Sum('total'))['total'] or 0,
            'total_paid': all_invoices.filter(status='paid').aggregate(total=Sum('total'))['total'] or 0,
            'pending_invoices': all_invoices.filter(status='sent').count(),
        }

        return context



class ClientCreateView(LoginRequiredMixin, CreateView):
    """Create a new client"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/create.html'
    success_url = reverse_lazy('clients:list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Client {form.instance.name} créé avec succès!')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing client"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/edit.html'
    success_url = reverse_lazy('clients:list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, f'Client {form.instance.name} mis à jour!')
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a client"""
    model = Client
    template_name = 'clients/confirm_delete.html'
    success_url = reverse_lazy('clients:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        client_name = self.get_object().name
        messages.success(request, f'Client {client_name} supprimé!')
        return super().delete(request, *args, **kwargs)
