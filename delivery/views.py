from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import DeliveryNote, DeliveryItem
from .forms import DeliveryNoteForm, DeliveryItemForm


class DeliveryNoteListView(LoginRequiredMixin, ListView):
    """List all delivery notes"""
    model = DeliveryNote
    template_name = 'delivery/list.html'
    context_object_name = 'deliveries'
    paginate_by = 20
    login_url = 'accounts:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(delivery_number__icontains=search) |
                Q(client__name__icontains=search)
            )

        return queryset


class DeliveryNoteDetailView(LoginRequiredMixin, DetailView):
    """Display delivery note details"""
    model = DeliveryNote
    template_name = 'delivery/detail.html'
    context_object_name = 'delivery'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('product').all()
        return context


class DeliveryNoteCreateView(LoginRequiredMixin, CreateView):
    """Create a new delivery note"""
    model = DeliveryNote
    form_class = DeliveryNoteForm
    template_name = 'delivery/create.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Bon de livraison {form.instance.delivery_number} créé!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('delivery:detail', kwargs={'pk': self.object.pk})


class DeliveryNoteUpdateView(LoginRequiredMixin, UpdateView):
    """Update a delivery note"""
    model = DeliveryNote
    form_class = DeliveryNoteForm
    template_name = 'delivery/edit.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, 'Bon de livraison mis à jour!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('delivery:detail', kwargs={'pk': self.object.pk})


class DeliveryNoteDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a delivery note"""
    model = DeliveryNote
    template_name = 'delivery/confirm_delete.html'
    success_url = reverse_lazy('delivery:list')
    login_url = 'accounts:login'

    def delete(self, request, *args, **kwargs):
        delivery_number = self.get_object().delivery_number
        messages.success(request, f'Bon de livraison {delivery_number} supprimé!')
        return super().delete(request, *args, **kwargs)
