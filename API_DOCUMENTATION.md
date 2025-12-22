# 📋 Invoice Management System - Complete API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Base URL](#base-url)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)
6. [Examples](#examples)
7. [Filters & Search](#filters--search)
8. [Pagination](#pagination)

---

## Authentication

### Token Authentication
All API requests (except `/api-token-auth/`) require a bearer token in the Authorization header.

#### Get Token
```
POST /api-token-auth/
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}

Response:
{
  "token": "abcdef123456..."
}
```

#### Use Token
```bash
Authorization: Token abcdef123456...
```

#### Token in curl
```bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/v1/...
```

#### Token in JavaScript
```javascript
const headers = {
  'Authorization': `Token ${token}`,
  'Content-Type': 'application/json'
};
```

---

## Base URL
```
http://127.0.0.1:8000/api/v1/
```

### API Versioning
Currently using v1. Future versions may be available at `/api/v2/`, etc.

---

## Response Format

### Successful Response (2xx)
```json
{
  "count": 120,
  "next": "http://127.0.0.1:8000/api/v1/endpoint/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "field": "value",
      ...
    }
  ]
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message here",
  "status_code": 400
}
```

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request successful | GET request returns data |
| 201 | Created - Resource created | POST creates new record |
| 204 | No Content - Successful, no response | DELETE successful |
| 400 | Bad Request - Invalid parameters | Missing required field |
| 401 | Unauthorized - No/invalid token | Token expired or missing |
| 403 | Forbidden - No permission | User role insufficient |
| 404 | Not Found - Resource doesn't exist | Invoice ID not found |
| 500 | Server Error - Backend issue | Database connection error |

### Error Response Example
```json
{
  "invoice_number": ["This field is required."],
  "client": ["This field is required."],
  "total": ["Ensure this value is greater than or equal to 0."]
}
```

---

## Endpoints

### User Profile
```
GET    /users/profile/              # List user profiles
POST   /users/profile/              # Create user profile
GET    /users/profile/{id}/         # Retrieve user profile
PUT    /users/profile/{id}/         # Update user profile
DELETE /users/profile/{id}/         # Delete user profile
GET    /users/profile/my_profile/   # Get current user profile
```

### Clients
```
GET    /clients/                    # List clients
POST   /clients/                    # Create client
GET    /clients/{id}/               # Retrieve client
PUT    /clients/{id}/               # Update client
PATCH  /clients/{id}/               # Partial update
DELETE /clients/{id}/               # Delete client
```

### Suppliers
```
GET    /suppliers/                  # List suppliers
POST   /suppliers/                  # Create supplier
GET    /suppliers/{id}/             # Retrieve supplier
PUT    /suppliers/{id}/             # Update supplier
PATCH  /suppliers/{id}/             # Partial update
DELETE /suppliers/{id}/             # Delete supplier
```

### Products
```
GET    /products/                   # List products
POST   /products/                   # Create product
GET    /products/{id}/              # Retrieve product
PUT    /products/{id}/              # Update product
PATCH  /products/{id}/              # Partial update
DELETE /products/{id}/              # Delete product
GET    /products/low_stock/         # Get low stock products
```

### Invoices
```
GET    /invoices/                   # List invoices
POST   /invoices/                   # Create invoice
GET    /invoices/{id}/              # Retrieve invoice
PUT    /invoices/{id}/              # Update invoice
PATCH  /invoices/{id}/              # Partial update
DELETE /invoices/{id}/              # Delete invoice
GET    /invoices/overdue/           # Get overdue invoices
POST   /invoices/{id}/mark_as_paid/        # Mark as paid
GET    /invoices/{id}/export_pdf/          # Export as PDF
GET    /invoices/{id}/export_excel/        # Export as Excel
GET    /invoices/export_all_excel/         # Export all as Excel
```

### Invoice Items
```
GET    /invoice-items/              # List invoice items
POST   /invoice-items/              # Create item
GET    /invoice-items/{id}/         # Retrieve item
PUT    /invoice-items/{id}/         # Update item
DELETE /invoice-items/{id}/         # Delete item
```

### Proforma Invoices
```
GET    /proforma-invoices/          # List proforma invoices
POST   /proforma-invoices/          # Create proforma
GET    /proforma-invoices/{id}/     # Retrieve proforma
PUT    /proforma-invoices/{id}/     # Update proforma
DELETE /proforma-invoices/{id}/     # Delete proforma
```

### Proforma Items
```
GET    /proforma-items/             # List items
POST   /proforma-items/             # Create item
GET    /proforma-items/{id}/        # Retrieve item
PUT    /proforma-items/{id}/        # Update item
DELETE /proforma-items/{id}/        # Delete item
```

### Delivery Notes
```
GET    /delivery-notes/             # List delivery notes
POST   /delivery-notes/             # Create delivery note
GET    /delivery-notes/{id}/        # Retrieve delivery note
PUT    /delivery-notes/{id}/        # Update delivery note
DELETE /delivery-notes/{id}/        # Delete delivery note
```

### Delivery Items
```
GET    /delivery-items/             # List delivery items
POST   /delivery-items/             # Create item
GET    /delivery-items/{id}/        # Retrieve item
PUT    /delivery-items/{id}/        # Update item
DELETE /delivery-items/{id}/        # Delete item
```

### Customer Orders
```
GET    /customer-orders/            # List customer orders
POST   /customer-orders/            # Create order
GET    /customer-orders/{id}/       # Retrieve order
PUT    /customer-orders/{id}/       # Update order
DELETE /customer-orders/{id}/       # Delete order
```

### Customer Order Items
```
GET    /customer-order-items/       # List order items
POST   /customer-order-items/       # Create item
GET    /customer-order-items/{id}/  # Retrieve item
PUT    /customer-order-items/{id}/  # Update item
DELETE /customer-order-items/{id}/  # Delete item
```

### Supplier Orders
```
GET    /supplier-orders/            # List supplier orders
POST   /supplier-orders/            # Create order
GET    /supplier-orders/{id}/       # Retrieve order
PUT    /supplier-orders/{id}/       # Update order
DELETE /supplier-orders/{id}/       # Delete order
```

### Supplier Order Items
```
GET    /supplier-order-items/       # List order items
POST   /supplier-order-items/       # Create item
GET    /supplier-order-items/{id}/  # Retrieve item
PUT    /supplier-order-items/{id}/  # Update item
DELETE /supplier-order-items/{id}/  # Delete item
```

### Payments
```
GET    /payments/                   # List payments
POST   /payments/                   # Create payment
GET    /payments/{id}/              # Retrieve payment
PUT    /payments/{id}/              # Update payment
DELETE /payments/{id}/              # Delete payment
```

### Analytics
```
GET    /dashboard/overview/         # Dashboard metrics
GET    /analytics/sales/            # Sales statistics
```

---

## Detailed Endpoint Reference

### 1. GET /invoices/
**List all invoices with pagination**

**Query Parameters:**
- `page`: Page number (default: 1)
- `status`: Invoice status (draft, sent, paid, partial, overdue, cancelled)
- `client`: Client UUID
- `invoice_date`: Exact date (YYYY-MM-DD)
- `invoice_date__gte`: Greater than or equal to date
- `invoice_date__lte`: Less than or equal to date
- `search`: Search by invoice_number, client name, description
- `ordering`: -invoice_date, -total, -created_at, invoice_date, total

**Example:**
```bash
GET /invoices/?status=paid&client=uuid&invoice_date__gte=2025-01-01&ordering=-invoice_date
```

**Response:**
```json
{
  "count": 45,
  "next": "http://...?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "invoice_number": "INV-2025-045",
      "client": "client-uuid",
      "client_name": "Acme Corporation",
      "invoice_date": "2025-12-22",
      "due_date": "2026-01-22",
      "status": "paid",
      "description": "Services rendered",
      "notes": "Thank you for your business",
      "subtotal": "5000.00",
      "tax_amount": "1000.00",
      "total": "6000.00",
      "paid_amount": "6000.00",
      "created_by": "admin",
      "created_at": "2025-12-20T10:30:00Z",
      "updated_at": "2025-12-21T15:45:00Z",
      "sent_at": "2025-12-20T11:00:00Z",
      "items": [
        {
          "id": "item-uuid",
          "invoice": "invoice-uuid",
          "product": "product-uuid",
          "product_name": "Web Development",
          "description": "Website redesign - 40 hours",
          "quantity": "40.00",
          "unit_price": "125.00",
          "tax_rate": "20.00",
          "subtotal": "5000.00",
          "tax": "1000.00",
          "total": "6000.00",
          "created_at": "2025-12-20T10:30:00Z"
        }
      ]
    }
  ]
}
```

### 2. POST /invoices/
**Create a new invoice**

**Request Body:**
```json
{
  "invoice_number": "INV-2025-046",
  "client": "client-uuid",
  "invoice_date": "2025-12-22",
  "due_date": "2026-01-22",
  "status": "draft",
  "description": "Monthly services",
  "notes": "Payment due within 30 days"
}
```

**Response:** 201 Created
```json
{
  "id": "invoice-uuid",
  "invoice_number": "INV-2025-046",
  "client": "client-uuid",
  ...
}
```

### 3. GET /invoices/{id}/
**Retrieve invoice details**

**Response:**
```json
{
  "id": "invoice-uuid",
  "invoice_number": "INV-2025-045",
  "client": "client-uuid",
  ...
  "items": [...]
}
```

### 4. PUT /invoices/{id}/
**Update invoice**

**Request Body:** (same as POST)
```json
{
  "invoice_number": "INV-2025-045",
  "status": "sent",
  ...
}
```

### 5. GET /invoices/{id}/export_pdf/
**Export invoice as PDF**

**Response:** PDF file download

### 6. GET /invoices/{id}/export_excel/
**Export invoice as Excel**

**Response:** Excel file download

### 7. POST /invoices/{id}/mark_as_paid/
**Mark invoice as paid**

**Response:**
```json
{
  "status": "Invoice marked as paid"
}
```

### 8. GET /dashboard/overview/
**Get dashboard metrics**

**Response:**
```json
{
  "total_invoices": 150250.00,
  "total_paid": 145100.00,
  "pending_invoices": 8,
  "overdue_invoices": 2,
  "month_invoiced": 25000.00,
  "month_paid": 23000.00,
  "total_clients": 45,
  "new_clients_this_month": 3,
  "low_stock_products": 5
}
```

### 9. GET /analytics/sales/
**Get monthly sales statistics**

**Response:**
```json
[
  {
    "month": "January 2025",
    "total": 12000.00
  },
  {
    "month": "February 2025",
    "total": 15000.00
  },
  ...
  {
    "month": "December 2025",
    "total": 28000.00
  }
]
```

### 10. GET /clients/
**List all clients**

**Query Parameters:**
- `page`: Page number
- `is_active`: true/false
- `city`: City name
- `country`: Country name
- `search`: Search by name, company, email, tax_id
- `ordering`: name, created_at, -created_at

**Response:**
```json
{
  "count": 45,
  "next": "...",
  "results": [
    {
      "id": "client-uuid",
      "name": "Acme Corporation",
      "company": "Acme Inc",
      "email": "contact@acme.com",
      "phone": "+1-555-1234",
      "fax": "+1-555-1235",
      "address": "123 Main St",
      "city": "New York",
      "postal_code": "10001",
      "country": "USA",
      "tax_id": "12-3456789",
      "website": "https://acme.com",
      "contact_person": "John Smith",
      "payment_terms": "Net 30",
      "credit_limit": "50000.00",
      "is_active": true,
      "notes": "Preferred client",
      "created_by": "admin",
      "created_at": "2025-01-15T08:00:00Z",
      "updated_at": "2025-12-20T14:30:00Z"
    }
  ]
}
```

### 11. POST /clients/
**Create new client**

**Request Body:**
```json
{
  "name": "New Client Ltd",
  "company": "New Client Inc",
  "email": "contact@newclient.com",
  "phone": "+1-555-9999",
  "address": "456 Oak Ave",
  "city": "Boston",
  "postal_code": "02101",
  "country": "USA",
  "tax_id": "98-7654321",
  "website": "https://newclient.com",
  "contact_person": "Jane Doe",
  "payment_terms": "Net 45",
  "credit_limit": "100000.00"
}
```

### 12. GET /products/
**List all products**

**Query Parameters:**
- `page`: Page number
- `is_active`: true/false
- `category`: Product category
- `search`: Search by name, sku, reference
- `ordering`: name, unit_price, quantity_in_stock

**Response:**
```json
{
  "count": 150,
  "results": [
    {
      "id": "product-uuid",
      "name": "Web Development Service",
      "description": "Professional web development",
      "sku": "WEB-DEV-001",
      "reference": "WD-001",
      "unit_price": "125.00",
      "cost_price": "50.00",
      "quantity_in_stock": 0,
      "reorder_level": 0,
      "tax_rate": "20.00",
      "category": "Services",
      "unit": "hour",
      "is_active": true,
      "is_low_stock": false,
      "created_by": "admin",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-12-20T10:00:00Z"
    }
  ]
}
```

### 13. GET /products/low_stock/
**Get products with low stock**

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": "product-uuid",
      "name": "Laptop Computer",
      "sku": "LAPTOP-001",
      "quantity_in_stock": 3,
      "reorder_level": 10,
      "is_low_stock": true,
      ...
    }
  ]
}
```

### 14. GET /payments/
**List all payments**

**Query Parameters:**
- `invoice`: Invoice UUID
- `method`: cash, check, bank_transfer, credit_card
- `payment_date__gte`: From date
- `payment_date__lte`: To date
- `ordering`: payment_date, amount, created_at

**Response:**
```json
{
  "count": 120,
  "results": [
    {
      "id": "payment-uuid",
      "invoice": "invoice-uuid",
      "invoice_number": "INV-2025-045",
      "payment_date": "2025-12-20",
      "amount": "6000.00",
      "method": "bank_transfer",
      "reference": "TRANSFER-12345",
      "notes": "Payment received",
      "created_by": "accountant",
      "created_at": "2025-12-20T10:30:00Z"
    }
  ]
}
```

---

## Examples

### Example 1: Create Complete Invoice with Items

```bash
# 1. Create invoice
curl -X POST http://127.0.0.1:8000/api/v1/invoices/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number": "INV-2025-050",
    "client": "client-uuid",
    "invoice_date": "2025-12-22",
    "due_date": "2026-01-22",
    "status": "draft"
  }'

# Response includes invoice ID

# 2. Add invoice items
curl -X POST http://127.0.0.1:8000/api/v1/invoice-items/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": "invoice-uuid",
    "product": "product-uuid",
    "description": "Web Development",
    "quantity": "40",
    "unit_price": "125",
    "tax_rate": "20"
  }'

# 3. Get invoice with calculated totals
curl http://127.0.0.1:8000/api/v1/invoices/invoice-uuid/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Example 2: Export Invoice

```bash
# Export as PDF
curl http://127.0.0.1:8000/api/v1/invoices/invoice-uuid/export_pdf/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -o invoice.pdf

# Export as Excel
curl http://127.0.0.1:8000/api/v1/invoices/invoice-uuid/export_excel/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -o invoice.xlsx

# Export all invoices
curl http://127.0.0.1:8000/api/v1/invoices/export_all_excel/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -o invoices_export.xlsx
```

### Example 3: Filter and Search Invoices

```bash
# Get paid invoices
curl http://127.0.0.1:8000/api/v1/invoices/?status=paid \
  -H "Authorization: Token YOUR_TOKEN"

# Get overdue invoices
curl http://127.0.0.1:8000/api/v1/invoices/overdue/ \
  -H "Authorization: Token YOUR_TOKEN"

# Search by invoice number
curl "http://127.0.0.1:8000/api/v1/invoices/?search=INV-2025" \
  -H "Authorization: Token YOUR_TOKEN"

# Date range filter
curl "http://127.0.0.1:8000/api/v1/invoices/?invoice_date__gte=2025-01-01&invoice_date__lte=2025-12-31" \
  -H "Authorization: Token YOUR_TOKEN"

# Complex filtering
curl "http://127.0.0.1:8000/api/v1/invoices/?status=sent&ordering=-invoice_date&page=2" \
  -H "Authorization: Token YOUR_TOKEN"
```

### Example 4: JavaScript API Client

```javascript
class InvoiceAPI {
  constructor(token, baseURL = 'http://127.0.0.1:8000/api/v1') {
    this.token = token;
    this.baseURL = baseURL;
  }

  async getInvoices(filters = {}) {
    const query = new URLSearchParams(filters);
    const response = await fetch(`${this.baseURL}/invoices/?${query}`, {
      headers: { 'Authorization': `Token ${this.token}` }
    });
    return response.json();
  }

  async createInvoice(data) {
    const response = await fetch(`${this.baseURL}/invoices/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async exportPDF(invoiceId) {
    const response = await fetch(`${this.baseURL}/invoices/${invoiceId}/export_pdf/`, {
      headers: { 'Authorization': `Token ${this.token}` }
    });
    return response.blob();
  }

  async getDashboard() {
    const response = await fetch(`${this.baseURL}/dashboard/overview/`, {
      headers: { 'Authorization': `Token ${this.token}` }
    });
    return response.json();
  }
}

// Usage
const api = new InvoiceAPI(token);
const invoices = await api.getInvoices({ status: 'paid' });
const dashboard = await api.getDashboard();
```

---

## Filters & Search

### Available Filter Operators

| Operator | Usage | Example |
|----------|-------|---------|
| `=` (exact) | Field value equals | `status=paid` |
| `__gte` | Greater than or equal | `invoice_date__gte=2025-01-01` |
| `__lte` | Less than or equal | `invoice_date__lte=2025-12-31` |
| `__gt` | Greater than | `total__gt=1000` |
| `__lt` | Less than | `total__lt=5000` |
| `__in` | Multiple values | `status__in=paid,sent` |

### Search Fields by Endpoint

| Endpoint | Searchable Fields |
|----------|------------------|
| `/invoices/` | invoice_number, client__name, description |
| `/clients/` | name, company, email, phone, tax_id |
| `/products/` | name, sku, reference, description |
| `/suppliers/` | name, company, email, phone, tax_id |
| `/payments/` | invoice__invoice_number, reference |

---

## Pagination

### Default Pagination
- **Items per page**: 20
- **Maximum**: 100 (configurable)

### Pagination Parameters
```
GET /invoices/?page=1
GET /invoices/?page=2
GET /invoices/?page=3
```

### Pagination Response
```json
{
  "count": 150,
  "next": "http://...?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Rate Limiting

Currently no rate limiting is enforced, but will be added for production.

Recommended limits:
- **API Requests**: 1000 requests per hour per user
- **File Exports**: 10 exports per hour per user

---

## Versioning

API version is specified in the URL path:
- Current: `/api/v1/`
- Future: `/api/v2/` (when available)

---

## Best Practices

1. **Always include authorization header**
2. **Use appropriate HTTP methods** (GET, POST, PUT, DELETE, PATCH)
3. **Check response status codes**
4. **Handle errors gracefully**
5. **Use pagination for large datasets**
6. **Cache tokens to avoid re-authentication**
7. **Use filtering to reduce response size**
8. **Validate data before sending**

---

**Last Updated**: December 22, 2025  
**API Version**: v1  
**Base URL**: http://127.0.0.1:8000/api/v1/  
**Authentication**: Token-based
