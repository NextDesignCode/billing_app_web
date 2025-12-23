from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import FileResponse
from datetime import timedelta
from accounts.models import UserProfile
from clients.models import Client
from suppliers.models import Supplier
from products.models import Product
from invoices.models import Invoice, InvoiceItem
from proforma.models import ProformaInvoice, ProformaItem
from delivery.models import DeliveryNote, DeliveryItem
from orders.models import CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem
from payments.models import Payment
from core.models import DashboardMetric

from .serializers import (
    UserProfileSerializer, ClientSerializer, SupplierSerializer, ProductSerializer,
    InvoiceSerializer, InvoiceItemSerializer, ProformaInvoiceSerializer, ProformaItemSerializer,
    DeliveryNoteSerializer, DeliveryItemSerializer, CustomerOrderSerializer, CustomerOrderItemSerializer,
    SupplierOrderSerializer, SupplierOrderItemSerializer, PaymentSerializer, DashboardMetricSerializer
)
from .exports import (
    generate_invoice_pdf, generate_invoice_excel, generate_invoices_list_excel,
    generate_proforma_pdf
)


# ============================================================================
# User & Authentication ViewSets
# ============================================================================

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'User profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================================
# Client ViewSet
# ============================================================================

class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clients
    """
    queryset = Client.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'city', 'country']
    search_fields = ['name', 'company', 'email', 'phone', 'tax_id']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Supplier ViewSet
# ============================================================================

class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing suppliers
    """
    queryset = Supplier.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'city', 'country']
    search_fields = ['name', 'company', 'email', 'phone', 'tax_id']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Product ViewSet
# ============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products
    """
    queryset = Product.objects.filter(is_active=True).order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'category']
    search_fields = ['name', 'sku', 'reference', 'description']
    ordering_fields = ['name', 'unit_price', 'quantity_in_stock']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock"""
        low_stock_products = self.queryset.filter(
            quantity_in_stock__lte=F('reorder_level')
        )
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


# ============================================================================
# Invoice ViewSets
# ============================================================================

class InvoiceItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for invoice line items
    """
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['invoice']


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing invoices
    """
    queryset = Invoice.objects.all().order_by('-invoice_date')
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client', 'invoice_date']
    search_fields = ['invoice_number', 'client__name', 'description']
    ordering_fields = ['invoice_date', 'total', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue invoices"""
        today = timezone.now().date()
        overdue_invoices = self.queryset.filter(
            due_date__lt=today,
            status__in=['sent', 'partial']
        )
        page = self.paginate_queryset(overdue_invoices)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(overdue_invoices, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        invoice.status = 'paid'
        invoice.paid_amount = invoice.total
        invoice.save()
        return Response({'status': 'Invoice marked as paid'})

    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        """Export invoice as PDF"""
        invoice = self.get_object()
        pdf_buffer = generate_invoice_pdf(invoice)
        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"Invoice_{invoice.invoice_number}.pdf",
            content_type='application/pdf'
        )

    @action(detail=True, methods=['get'])
    def export_excel(self, request, pk=None):
        """Export invoice as Excel"""
        invoice = self.get_object()
        excel_buffer = generate_invoice_excel(invoice)
        return FileResponse(
            excel_buffer,
            as_attachment=True,
            filename=f"Invoice_{invoice.invoice_number}.xlsx",
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    @action(detail=False, methods=['get'])
    def export_all_excel(self, request):
        """Export all invoices as Excel"""
        invoices = self.filter_queryset(self.get_queryset())
        excel_buffer = generate_invoices_list_excel(invoices)
        return FileResponse(
            excel_buffer,
            as_attachment=True,
            filename=f"Invoices_Export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


# ============================================================================
# Proforma Invoice ViewSets
# ============================================================================

class ProformaItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for proforma invoice line items
    """
    queryset = ProformaItem.objects.all()
    serializer_class = ProformaItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['proforma']


class ProformaInvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing proforma invoices
    """
    queryset = ProformaInvoice.objects.all().order_by('-issue_date')
    serializer_class = ProformaInvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client', 'issue_date']
    search_fields = ['proforma_number', 'client__name', 'description']
    ordering_fields = ['issue_date', 'total', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Delivery Notes ViewSets
# ============================================================================

class DeliveryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for delivery note line items
    """
    queryset = DeliveryItem.objects.all()
    serializer_class = DeliveryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['delivery_note']


class DeliveryNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing delivery notes
    """
    queryset = DeliveryNote.objects.all().order_by('-delivery_date')
    serializer_class = DeliveryNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client', 'delivery_date']
    search_fields = ['delivery_number', 'client__name', 'description']
    ordering_fields = ['delivery_date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Customer Orders ViewSets
# ============================================================================

class CustomerOrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for customer order line items
    """
    queryset = CustomerOrderItem.objects.all()
    serializer_class = CustomerOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']


class CustomerOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customer orders
    """
    queryset = CustomerOrder.objects.all().order_by('-order_date')
    serializer_class = CustomerOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client', 'order_date']
    search_fields = ['order_number', 'client__name', 'description']
    ordering_fields = ['order_date', 'total', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Supplier Orders ViewSets
# ============================================================================

class SupplierOrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for supplier order line items
    """
    queryset = SupplierOrderItem.objects.all()
    serializer_class = SupplierOrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']


class SupplierOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing supplier orders
    """
    queryset = SupplierOrder.objects.all().order_by('-order_date')
    serializer_class = SupplierOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'supplier', 'order_date']
    search_fields = ['purchase_order_number', 'supplier__name', 'description']
    ordering_fields = ['order_date', 'total', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Payment ViewSet
# ============================================================================

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing payments
    """
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['invoice', 'method', 'payment_date']
    ordering_fields = ['payment_date', 'amount', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================================
# Dashboard Analytics
# ============================================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """Get dashboard overview with key metrics"""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Calculate metrics
    total_invoices = Invoice.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_paid = Invoice.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    pending_invoices = Invoice.objects.filter(status__in=['sent', 'partial']).count()
    overdue_invoices = Invoice.objects.filter(
        due_date__lt=today,
        status__in=['sent', 'partial']
    ).count()

    # Monthly metrics
    month_invoiced = Invoice.objects.filter(
        invoice_date__gte=start_of_month
    ).aggregate(Sum('total'))['total__sum'] or 0

    month_paid = Payment.objects.filter(
        payment_date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Client metrics
    total_clients = Client.objects.filter(is_active=True).count()
    new_clients_this_month = Client.objects.filter(
        created_at__gte=start_of_month
    ).count()

    # Product metrics
    low_stock_products = Product.objects.filter(
        quantity_in_stock__lte=F('reorder_level')
    ).count()

    return Response({
        'total_invoices': float(total_invoices),
        'total_paid': float(total_paid),
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'month_invoiced': float(month_invoiced),
        'month_paid': float(month_paid),
        'total_clients': total_clients,
        'new_clients_this_month': new_clients_this_month,
        'low_stock_products': low_stock_products,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_statistics(request):
    """Get sales statistics for the past 12 months"""
    today = timezone.now().date()

    # Generate statistics for last 12 months
    statistics = []
    for i in range(11, -1, -1):
        month_start = today - timedelta(days=today.day + i*30)
        month_start = month_start.replace(day=1)

        next_month = month_start + timedelta(days=31)
        next_month = next_month.replace(day=1)

        monthly_total = Invoice.objects.filter(
            invoice_date__gte=month_start,
            invoice_date__lt=next_month
        ).aggregate(Sum('total'))['total__sum'] or 0

        statistics.append({
            'month': month_start.strftime('%B %Y'),
            'total': float(monthly_total),
        })

    return Response(statistics)
