# ============================================================================
# accounts/views.py
# ============================================================================
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomLoginForm, UserProfileForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:dashboard')


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('accounts:login')


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
