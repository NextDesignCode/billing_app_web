# ============================================================================
# accounts/views.py
# ============================================================================
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from .forms import CustomLoginForm, UserProfileForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Connexion réussie! Bienvenue.')
        return super().form_valid(form)


class CustomLogoutView(TemplateView):
    """Custom logout view with template"""
    template_name = 'accounts/logout.html'

    def dispatch(self, request, *args, **kwargs):
        # Store the username before logout for message
        username = request.user.username if request.user.is_authenticated else None

        # Logout the user
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, f'Au revoir {username} ! Vous avez été déconnecté.')

        # Pass an empty context without user
        return render(request, self.template_name, {
            'current_year': datetime.now().year,
            'site_name': 'Facturation Pro',
            'site_version': '1.0.0',
            # Don't pass user or pass AnonymousUser
        })

class ProfileView(LoginRequiredMixin, UpdateView):
    """View and edit user profile"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    login_url = 'accounts:login'

    def get_object(self, queryset=None):
        # Get or create profile for current user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, 'Profil mis à jour avec succès!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'current_year': datetime.now().year,
            'site_name': 'Facturation Pro',
            'site_version': '1.0.0',
        })
        return context
