from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated

from .models import (
    Invoice, Client, Supplier, Product, Payment,
    ProformaInvoice, DeliveryNote, CustomerOrder, SupplierOrder
)


# ================== Authentication Views ==================

class CustomLoginView(LoginView):
    """Vue de connexion personnalisée"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('core:dashboard')


class CustomLogoutView(LogoutView):
    """Vue de déconnexion"""
    next_page = reverse_lazy('core:login')


# ================== Dashboard & Home Views ==================

@login_required(login_url='core:login')
def dashboard(request):
    """
    Vue du tableau de bord principal
    Affiche les métriques clés et les données récentes
    """
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    today = timezone.now().date()

    # Métriques principales
    context = {
        # Facturation
        'total_invoiced': Invoice.objects.filter(status__in=['sent', 'paid']).aggregate(
            total=Sum('total')
        )['total'] or 0,

        'total_paid': Invoice.objects.filter(status='paid').aggregate(
            total=Sum('total')
        )['total'] or 0,

        'pending_count': Invoice.objects.filter(status='sent').count(),

        'overdue_count': Invoice.objects.filter(
            status__in=['sent', 'partial'],
            due_date__lt=today
        ).count(),

        # Clients & Fournisseurs
        'total_clients': Client.objects.filter(is_active=True).count(),
        'total_suppliers': Supplier.objects.filter(is_active=True).count(),

        # Produits
        'total_products': Product.objects.count(),
        'low_stock_products': Product.objects.filter(
            quantity_in_stock__lte=models.F('reorder_level')
        ).count(),

        # Commandes
        'pending_orders': CustomerOrder.objects.filter(status='pending').count(),
        'pending_supplier_orders': SupplierOrder.objects.filter(status='pending').count(),

        # Récentes données
        'recent_invoices': Invoice.objects.select_related('client').order_by('-created_at')[:5],
        'recent_payments': Payment.objects.select_related('invoice').order_by('-created_at')[:5],
        'low_stock_items': Product.objects.filter(
            quantity_in_stock__lte=models.F('reorder_level')
        )[:5],

        'user_profile': user_profile,
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='core:login')
def home(request):
    """Redirection vers le tableau de bord"""
    return redirect('core:dashboard')


# ================== Invoice Views ==================

@login_required(login_url='core:login')
def invoice_list(request):
    """Liste des factures avec filtrage"""
    invoices = Invoice.objects.select_related('client').order_by('-created_at')

    # Filtrage par statut
    status = request.GET.get('status')
    if status:
        invoices = invoices.filter(status=status)

    # Filtrage par client
    client_id = request.GET.get('client')
    if client_id:
        invoices = invoices.filter(client_id=client_id)

    # Recherche
    search = request.GET.get('search')
    if search:
        invoices = invoices.filter(
            Q(number__icontains=search) |
            Q(client__name__icontains=search)
        )

    context = {
        'invoices': invoices,
        'clients': Client.objects.filter(is_active=True),
        'status_choices': Invoice.STATUS_CHOICES,
    }
    return render(request, 'invoices/list.html', context)


@login_required(login_url='core:login')
def invoice_detail(request, pk):
    """Détail d'une facture"""
    invoice = get_object_or_404(Invoice, pk=pk)

    context = {
        'invoice': invoice,
        'items': invoice.items.all(),
    }
    return render(request, 'invoices/detail.html', context)


# ================== Client Views ==================

@login_required(login_url='core:login')
def client_list(request):
    """Liste des clients"""
    clients = Client.objects.all().order_by('name')

    # Filtrage par statut
    active_only = request.GET.get('active')
    if active_only:
        clients = clients.filter(is_active=True)

    # Recherche
    search = request.GET.get('search')
    if search:
        clients = clients.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(tax_id__icontains=search)
        )

    context = {
        'clients': clients,
    }
    return render(request, 'clients/list.html', context)


@login_required(login_url='core:login')
def client_detail(request, pk):
    """Détail d'un client"""
    client = get_object_or_404(Client, pk=pk)
    invoices = client.invoices.all().order_by('-created_at')

    # Statistiques client
    stats = {
        'total_invoiced': invoices.aggregate(total=Sum('total'))['total'] or 0,
        'total_paid': invoices.filter(status='paid').aggregate(total=Sum('total'))['total'] or 0,
        'pending_invoices': invoices.filter(status='sent').count(),
    }

    context = {
        'client': client,
        'invoices': invoices[:10],
        'stats': stats,
    }
    return render(request, 'clients/detail.html', context)


# ================== Product Views ==================

@login_required(login_url='core:login')
def product_list(request):
    """Liste des produits"""
    products = Product.objects.all().order_by('name')

    # Filtrage par catégorie
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    # Filtrer produits en rupture de stock
    low_stock = request.GET.get('low_stock')
    if low_stock:
        products = products.filter(quantity_in_stock__lte=models.F('reorder_level'))

    # Recherche
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search)
        )

    context = {
        'products': products,
        'categories': Product.objects.values_list('category', flat=True).distinct(),
    }
    return render(request, 'products/list.html', context)


@login_required(login_url='core:login')
def product_detail(request, pk):
    """Détail d'un produit"""
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product,
    }
    return render(request, 'products/detail.html', context)


# ================== Payment Views ==================

@login_required(login_url='core:login')
def payment_list(request):
    """Liste des paiements"""
    payments = Payment.objects.select_related('invoice').order_by('-created_at')

    # Filtrage par méthode
    method = request.GET.get('method')
    if method:
        payments = payments.filter(payment_method=method)

    # Recherche
    search = request.GET.get('search')
    if search:
        payments = payments.filter(
            Q(invoice__number__icontains=search) |
            Q(reference_number__icontains=search)
        )

    context = {
        'payments': payments,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'payments/list.html', context)


# ================== Supplier Views ==================

@login_required(login_url='core:login')
def supplier_list(request):
    """Liste des fournisseurs"""
    suppliers = Supplier.objects.all().order_by('name')

    # Filtrage par statut
    active_only = request.GET.get('active')
    if active_only:
        suppliers = suppliers.filter(is_active=True)

    # Recherche
    search = request.GET.get('search')
    if search:
        suppliers = suppliers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    context = {
        'suppliers': suppliers,
    }
    return render(request, 'suppliers/list.html', context)


# ================== Utility Views ==================

@login_required(login_url='core:login')
def search(request):
    """Vue de recherche globale"""
    query = request.GET.get('q', '')

    results = {
        'invoices': Invoice.objects.filter(
            Q(number__icontains=query) |
            Q(client__name__icontains=query)
        )[:5],
        'clients': Client.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )[:5],
        'products': Product.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query)
        )[:5],
        'suppliers': Supplier.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query)
        )[:5],
    }

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)


@login_required(login_url='core:login')
def reports(request):
    """Vue des rapports"""
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)

    context = {
        'monthly_revenue': Invoice.objects.filter(
            created_at__gte=month_ago,
            status='paid'
        ).aggregate(total=Sum('total'))['total'] or 0,

        'monthly_invoices': Invoice.objects.filter(
            created_at__gte=month_ago
        ).count(),

        'monthly_clients': Client.objects.filter(
            created_at__gte=month_ago
        ).count(),
    }
    return render(request, 'reports.html', context)


from django.db import models
