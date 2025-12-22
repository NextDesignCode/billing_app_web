from rest_framework import serializers
from core.models import (
    UserProfile, Client, Supplier, Product, Invoice, InvoiceItem,
    ProformaInvoice, ProformaItem, DeliveryNote, DeliveryItem,
    CustomerOrder, CustomerOrderItem, SupplierOrder, SupplierOrderItem,
    Payment, DashboardMetric
)
from django.contrib.auth.models import User


# ============================================================================
# User & Authentication Serializers
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


# ============================================================================
# Client & Supplier Serializers
# ============================================================================

class ClientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


class SupplierSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Product Serializer
# ============================================================================

class ProductSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')
    
    def get_is_low_stock(self, obj):
        return obj.is_low_stock()


# ============================================================================
# Invoice Serializers
# ============================================================================

class InvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax', 'total', 'created_at')


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Proforma Invoices Serializers
# ============================================================================

class ProformaItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProformaItem
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax', 'total', 'created_at')


class ProformaInvoiceSerializer(serializers.ModelSerializer):
    items = ProformaItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ProformaInvoice
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Delivery Notes Serializers
# ============================================================================

class DeliveryItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = DeliveryItem
        fields = '__all__'
        read_only_fields = ('id',)


class DeliveryNoteSerializer(serializers.ModelSerializer):
    items = DeliveryItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = DeliveryNote
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Customer Orders Serializers
# ============================================================================

class CustomerOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = CustomerOrderItem
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax', 'total')


class CustomerOrderSerializer(serializers.ModelSerializer):
    items = CustomerOrderItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = CustomerOrder
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Supplier Orders Serializers
# ============================================================================

class SupplierOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = SupplierOrderItem
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax', 'total')


class SupplierOrderSerializer(serializers.ModelSerializer):
    items = SupplierOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = SupplierOrder
        fields = '__all__'
        read_only_fields = ('id', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at', 'created_by')


# ============================================================================
# Payment Serializer
# ============================================================================

class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')


# ============================================================================
# Dashboard Metrics Serializer
# ============================================================================

class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
