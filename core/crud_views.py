"""
Views CRUD complets pour la gestion des factures, clients, produits, etc.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.db.models import Q
from decimal import Decimal
from io import BytesIO

from invoices.models import Invoice, InvoiceItem
from clients.models import Client
from suppliers.models import Supplier
from products.models import Product
from payments.models import Payment
from proforma.models import ProformaInvoice, ProformaItem
from delivery.models import DeliveryNote, DeliveryItem
from orders.models import CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem

from api.exports import (
    generate_invoice_pdf, generate_invoice_excel,
    generate_proforma_pdf, generate_proforma_excel
)


# ==================== INVOICES ====================

@login_required(login_url='accounts:login')
def invoice_create(request):
    """Créer une nouvelle facture"""
    if request.method == 'POST':
        client_id = request.POST.get('client')
        invoice_date = request.POST.get('invoice_date')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')

        invoice = Invoice.objects.create(
            client_id=client_id,
            invoice_date=invoice_date,
            due_date=due_date,
            description=description,
            created_by=request.user,
            status='draft'
        )
        messages.success(request, f'Facture {invoice.invoice_number} créée avec succès!')
        return redirect('core:invoice_detail', pk=invoice.pk)

    clients = Client.objects.filter(is_active=True)
    return render(request, 'invoices/create.html', {'clients': clients})


@login_required(login_url='accounts:login')
def invoice_edit(request, pk):
    """Éditer une facture"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.due_date = request.POST.get('due_date')
        invoice.description = request.POST.get('description')
        invoice.status = request.POST.get('status')
        invoice.save()

        messages.success(request, 'Facture mise à jour!')
        return redirect('core:invoice_detail', pk=invoice.pk)

    return render(request, 'invoices/edit.html', {'invoice': invoice})


@login_required(login_url='accounts:login')
def invoice_delete(request, pk):
    """Supprimer une facture"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Facture {invoice_number} supprimée!')
        return redirect('core:invoice_list')

    return render(request, 'invoices/confirm_delete.html', {'invoice': invoice})


@login_required(login_url='accounts:login')
def invoice_add_item(request, pk):
    """Ajouter un article à une facture"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        unit_price = Decimal(request.POST.get('unit_price', 0))

        product = Product.objects.get(id=product_id)
        if unit_price == 0:
            unit_price = product.unit_price

        item = InvoiceItem.objects.create(
            invoice=invoice,
            product=product,
            quantity=quantity,
            unit_price=unit_price
        )

        messages.success(request, f'{product.name} ajouté à la facture!')
        return redirect('core:invoice_detail', pk=invoice.pk)

    products = Product.objects.filter(is_active=True)
    return render(request, 'invoices/add_item.html', {
        'invoice': invoice,
        'products': products
    })


@login_required(login_url='accounts:login')
def invoice_export_pdf(request, pk):
    """Exporter une facture en PDF"""
    invoice = get_object_or_404(Invoice, pk=pk)
    pdf_buffer = generate_invoice_pdf(invoice)

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{invoice.invoice_number}.pdf"'
    return response


@login_required(login_url='accounts:login')
def invoice_export_excel(request, pk):
    """Exporter une facture en Excel"""
    invoice = get_object_or_404(Invoice, pk=pk)
    excel_buffer = generate_invoice_excel(invoice)

    response = HttpResponse(
        excel_buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="facture_{invoice.invoice_number}.xlsx"'
    return response


# ==================== PROFORMA ====================

@login_required(login_url='accounts:login')
def proforma_list(request):
    """Liste des devis proforma"""
    proformas = ProformaInvoice.objects.select_related('client').order_by('-created_at')

    search = request.GET.get('search')
    if search:
        proformas = proformas.filter(
            Q(number__icontains=search) |
            Q(client__name__icontains=search)
        )

    return render(request, 'proforma/list.html', {'proformas': proformas})


@login_required(login_url='accounts:login')
def proforma_detail(request, pk):
    """Détail d'une proforma"""
    proforma = get_object_or_404(ProformaInvoice, pk=pk)
    return render(request, 'proforma/detail.html', {'proforma': proforma})


@login_required(login_url='accounts:login')
def proforma_create(request):
    """Créer une nouvelle proforma"""
    if request.method == 'POST':
        client_id = request.POST.get('client')
        proforma = ProformaInvoice.objects.create(
            client_id=client_id,
            created_by=request.user
        )
        messages.success(request, 'Proforma créée!')
        return redirect('core:proforma_detail', pk=proforma.pk)

    clients = Client.objects.filter(is_active=True)
    return render(request, 'proforma/create.html', {'clients': clients})


# ==================== DELIVERY NOTES ====================

@login_required(login_url='accounts:login')
def delivery_list(request):
    """Liste des bons de livraison"""
    deliveries = DeliveryNote.objects.select_related('client').order_by('-created_at')

    search = request.GET.get('search')
    if search:
        deliveries = deliveries.filter(
            Q(number__icontains=search) |
            Q(client__name__icontains=search)
        )

    return render(request, 'delivery/list.html', {'deliveries': deliveries})


@login_required(login_url='accounts:login')
def delivery_detail(request, pk):
    """Détail d'un bon de livraison"""
    delivery = get_object_or_404(DeliveryNote, pk=pk)
    return render(request, 'delivery/detail.html', {'delivery': delivery})


@login_required(login_url='accounts:login')
def delivery_create(request):
    """Créer un nouveau bon de livraison"""
    if request.method == 'POST':
        client_id = request.POST.get('client')
        invoice_id = request.POST.get('invoice')

        delivery = DeliveryNote.objects.create(
            client_id=client_id,
            created_by=request.user
        )

        if invoice_id:
            delivery.related_invoice_id = invoice_id
            delivery.save()

        messages.success(request, 'Bon de livraison créé!')
        return redirect('core:delivery_detail', pk=delivery.pk)

    clients = Client.objects.filter(is_active=True)
    invoices = Invoice.objects.filter(status__in=['sent', 'partial'])

    return render(request, 'delivery/create.html', {
        'clients': clients,
        'invoices': invoices
    })


# ==================== CUSTOMER ORDERS ====================

@login_required(login_url='accounts:login')
def customer_order_list(request):
    """Liste des commandes clients"""
    orders = CustomerOrder.objects.select_related('client').order_by('-created_at')

    search = request.GET.get('search')
    status_filter = request.GET.get('status')

    if search:
        orders = orders.filter(
            Q(number__icontains=search) |
            Q(client__name__icontains=search)
        )

    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'orders/customer_list.html', {
        'orders': orders,
        'status_choices': CustomerOrder.STATUS_CHOICES
    })


@login_required(login_url='accounts:login')
def customer_order_detail(request, pk):
    """Détail d'une commande client"""
    order = get_object_or_404(CustomerOrder, pk=pk)
    return render(request, 'orders/customer_detail.html', {'order': order})


@login_required(login_url='accounts:login')
def customer_order_create(request):
    """Créer une nouvelle commande client"""
    if request.method == 'POST':
        client_id = request.POST.get('client')
        order_date = request.POST.get('order_date')

        order = CustomerOrder.objects.create(
            client_id=client_id,
            order_date=order_date,
            created_by=request.user,
            status='pending'
        )

        messages.success(request, 'Commande créée!')
        return redirect('core:customer_order_detail', pk=order.pk)

    clients = Client.objects.filter(is_active=True)
    return render(request, 'orders/customer_create.html', {'clients': clients})


# ==================== CLIENTS ====================

@login_required(login_url='accounts:login')
def client_create(request):
    """Créer un nouveau client"""
    if request.method == 'POST':
        client = Client.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            postal_code=request.POST.get('postal_code'),
            tax_id=request.POST.get('tax_id'),
            is_active=True
        )
        messages.success(request, f'Client {client.name} créé!')
        return redirect('core:client_detail', pk=client.pk)

    return render(request, 'clients/create.html')


@login_required(login_url='accounts:login')
def client_edit(request, pk):
    """Éditer un client"""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.address = request.POST.get('address')
        client.city = request.POST.get('city')
        client.country = request.POST.get('country')
        client.postal_code = request.POST.get('postal_code')
        client.tax_id = request.POST.get('tax_id')
        client.save()

        messages.success(request, 'Client mis à jour!')
        return redirect('core:client_detail', pk=client.pk)

    return render(request, 'clients/edit.html', {'client': client})


@login_required(login_url='accounts:login')
def client_delete(request, pk):
    """Supprimer un client"""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Client {name} supprimé!')
        return redirect('core:client_list')

    return render(request, 'clients/confirm_delete.html', {'client': client})


# ==================== PRODUCTS ====================

@login_required(login_url='accounts:login')
def product_create(request):
    """Créer un nouveau produit"""
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            category=request.POST.get('category'),
            unit_price=Decimal(request.POST.get('unit_price', 0)),
            cost_price=Decimal(request.POST.get('cost_price', 0)),
            quantity_in_stock=int(request.POST.get('quantity_in_stock', 0)),
            reorder_level=int(request.POST.get('reorder_level', 0)),
            tax_rate=Decimal(request.POST.get('tax_rate', 0)),
            is_active=True
        )
        messages.success(request, f'Produit {product.name} créé!')
        return redirect('core:product_detail', pk=product.pk)

    return render(request, 'products/create.html')


@login_required(login_url='accounts:login')
def product_edit(request, pk):
    """Éditer un produit"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.category = request.POST.get('category')
        product.unit_price = Decimal(request.POST.get('unit_price', 0))
        product.cost_price = Decimal(request.POST.get('cost_price', 0))
        product.quantity_in_stock = int(request.POST.get('quantity_in_stock', 0))
        product.reorder_level = int(request.POST.get('reorder_level', 0))
        product.tax_rate = Decimal(request.POST.get('tax_rate', 0))
        product.save()

        messages.success(request, 'Produit mis à jour!')
        return redirect('core:product_detail', pk=product.pk)

    return render(request, 'products/edit.html', {'product': product})


@login_required(login_url='accounts:login')
def product_delete(request, pk):
    """Supprimer un produit"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Produit {name} supprimé!')
        return redirect('core:product_list')

    return render(request, 'products/confirm_delete.html', {'product': product})


# ==================== SUPPLIERS ====================

@login_required(login_url='accounts:login')
def supplier_create(request):
    """Créer un nouveau fournisseur"""
    if request.method == 'POST':
        supplier = Supplier.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            tax_id=request.POST.get('tax_id'),
            created_by=request.user,
            is_active=True
        )
        messages.success(request, f'Fournisseur {supplier.name} créé!')
        return redirect('core:supplier_list')

    return render(request, 'suppliers/create.html', {})


@login_required(login_url='accounts:login')
def supplier_edit(request, pk):
    """Éditer un fournisseur"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.email = request.POST.get('email')
        supplier.phone = request.POST.get('phone')
        supplier.address = request.POST.get('address')
        supplier.postal_code = request.POST.get('postal_code')
        supplier.city = request.POST.get('city')
        supplier.country = request.POST.get('country')
        supplier.tax_id = request.POST.get('tax_id')
        supplier.save()
        messages.success(request, f'Fournisseur {supplier.name} modifié!')
        return redirect('core:supplier_list')

    return render(request, 'suppliers/edit.html', {'supplier': supplier})


@login_required(login_url='accounts:login')
def supplier_delete(request, pk):
    """Supprimer un fournisseur"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        name = supplier.name
        supplier.delete()
        messages.success(request, f'Fournisseur {name} supprimé!')
        return redirect('core:supplier_list')

    return render(request, 'suppliers/confirm_delete.html', {'supplier': supplier})


# ==================== PAYMENTS ====================

@login_required(login_url='accounts:login')
def payment_create(request):
    """Créer un nouveau paiement"""
    if request.method == 'POST':
        payment = Payment.objects.create(
            invoice_id=request.POST.get('invoice'),
            amount=Decimal(request.POST.get('amount', 0)),
            payment_method=request.POST.get('payment_method'),
            payment_date=request.POST.get('payment_date'),
            reference_number=request.POST.get('reference_number'),
            created_by=request.user
        )
        messages.success(request, f'Paiement de {payment.amount} € enregistré!')
        return redirect('core:payment_list')

    invoices = Invoice.objects.filter(status__in=['sent', 'partial']).order_by('-created_at')
    return render(request, 'payments/create.html', {'invoices': invoices})


# ==================== MISC ====================

@login_required(login_url='accounts:login')
def payment_list(request):
    """Liste les paiements"""
    payments = Payment.objects.all().order_by('-payment_date')

    if search := request.GET.get('search'):
        payments = payments.filter(
            Q(invoice__invoice_number__icontains=search) |
            Q(reference_number__icontains=search)
        )

    return render(request, 'payments/list.html', {'payments': payments})


@login_required(login_url='accounts:login')
def supplier_list(request):
    """Liste les fournisseurs"""
    suppliers = Supplier.objects.filter(is_active=True).order_by('name')

    if search := request.GET.get('search'):
        suppliers = suppliers.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    return render(request, 'suppliers/list.html', {'suppliers': suppliers})
