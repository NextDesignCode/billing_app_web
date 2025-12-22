# 📊 Professional Invoice Management System

A complete, production-ready invoice management application built with **Django REST Framework** backend and modern **HTML5 + Tailwind CSS** frontend.

---

## 🎯 Key Features

### ✅ Complete Invoicing System
- **Invoice Management**: Full CRUD with status tracking (Draft, Sent, Paid, Partial, Overdue, Cancelled)
- **Proforma Invoices**: Quotation system with independent lifecycle
- **Delivery Notes**: Track shipments and deliveries
- **Customer Orders**: Order management from quotes to fulfillment
- **Supplier Orders**: Purchase order management with receipt tracking
- **Payment Tracking**: Multiple payment methods, reconciliation, and history

### ✅ Business Management
- **Client Management**: Complete contact information, tax IDs, credit limits, payment terms
- **Supplier Management**: Vendor management with payment terms and contact details
- **Product Catalog**: SKU-based products with stock management, pricing, and tax rates
- **Stock Management**: Low stock alerts, reorder levels, inventory tracking

### ✅ Export & Reporting
- **PDF Export**: Professional invoice PDFs with proper formatting
- **Excel Export**: Detailed invoices and batch invoice lists
- **Dashboard Analytics**: KPIs, monthly statistics, sales trends
- **Advanced Search**: Filter and search across all documents
- **Low Stock Alerts**: Real-time inventory warnings

### ✅ User & Security
- **Role-Based Access**: Admin, Manager, User, Accountant roles
- **Token Authentication**: Secure API access with token authentication
- **User Profiles**: Extended user management with company information
- **Audit Trail**: Creation timestamps and user tracking for all records

### ✅ International Support
- **Multi-Language**: French and English support
- **Localization**: Translated model names, form labels, and messages
- **Regional Settings**: Currency, timezone, and date format support

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git

### Installation

1. **Clone or navigate to project**
```bash
cd "g:\Training de formations Udemy\Modern HTML-CSS"
```

2. **Activate Virtual Environment**
```bash
# Windows
invoice_env\Scripts\activate

# Linux/Mac
source invoice_env/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts to create admin account
```

5. **Collect Static Files** (Optional for development)
```bash
python manage.py collectstatic --noinput
```

6. **Start Development Server**
```bash
python manage.py runserver
```

The application will be available at:
- **Web Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/v1/

---

## 📝 Project Structure

```
invoice_project/
├── manage.py                  # Django management script
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
├── PROJECT_SETUP.md          # Detailed setup documentation
│
├── invoice_project/          # Main Django project
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
│
├── core/                     # Core business logic
│   ├── models.py            # Database models
│   ├── admin.py             # Admin interface configuration
│   ├── signals.py           # Signal handlers
│   └── migrations/          # Database migrations
│
├── api/                      # REST API
│   ├── views.py             # API ViewSets
│   ├── serializers.py       # Data serializers
│   ├── urls.py              # API routing
│   ├── exports.py           # PDF/Excel export functions
│   └── migrations/
│
├── templates/               # HTML templates
│   └── dashboard.html       # Main dashboard
│
├── static/                  # Static files (CSS, JS)
│   ├── css/
│   │   ├── tailwind.css
│   │   └── custom.css
│   └── js/
│       ├── app.js
│       ├── api.js
│       └── utils.js
│
├── media/                   # User uploads
│   ├── products/
│   └── documents/
│
└── invoice_env/             # Virtual environment
    └── ...
```

---

## 🔧 Technology Stack

### Backend
- **Django 6.0**: Python web framework
- **Django REST Framework 3.16**: API development
- **Python 3.11+**: Programming language
- **SQLite3**: Database (development)
- **ReportLab 4.4.7**: PDF generation
- **OpenPyXL 3.1.5**: Excel generation

### Frontend
- **HTML5**: Markup language
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript (ES6+)**: Client-side interactivity
- **Chart.js**: Data visualization

### Infrastructure
- **django-cors-headers**: CORS support for API
- **django-filter**: Advanced filtering
- **rest_framework.authtoken**: Token authentication
- **django-extensions**: Development utilities

---

## 📊 Database Models

### Core Entities
```
User (Django)
├── UserProfile (Extended profile with roles)

Client (Customers)
├── name, company, contact info
├── address, tax_id, credit_limit
└── payment_terms

Supplier (Vendors)
├── name, company, contact info
├── address, tax_id
└── payment_terms

Product (Catalog)
├── name, sku, reference
├── pricing (unit_price, cost_price)
├── stock management
└── tax_rate, category

Document Models:
├── Invoice → InvoiceItem → Product
├── ProformaInvoice → ProformaItem → Product
├── DeliveryNote → DeliveryItem → Product
├── CustomerOrder → CustomerOrderItem → Product
├── SupplierOrder → SupplierOrderItem → Product
└── Payment → Invoice

Reporting:
└── DashboardMetric (Aggregated statistics)
```

---

## 🔑 API Endpoints

### Authentication
```
POST   /api-token-auth/              # Get authentication token
```

### Clients
```
GET    /api/v1/clients/              # List clients
POST   /api/v1/clients/              # Create client
GET    /api/v1/clients/{id}/         # Get client details
PUT    /api/v1/clients/{id}/         # Update client
DELETE /api/v1/clients/{id}/         # Delete client
```

### Invoices
```
GET    /api/v1/invoices/             # List invoices
POST   /api/v1/invoices/             # Create invoice
GET    /api/v1/invoices/{id}/        # Get invoice details
PUT    /api/v1/invoices/{id}/        # Update invoice
DELETE /api/v1/invoices/{id}/        # Delete invoice
GET    /api/v1/invoices/overdue/     # Get overdue invoices
POST   /api/v1/invoices/{id}/mark_as_paid/  # Mark as paid
GET    /api/v1/invoices/{id}/export_pdf/    # Export PDF
GET    /api/v1/invoices/{id}/export_excel/  # Export Excel
GET    /api/v1/invoices/export_all_excel/   # Export all
```

### Suppliers
```
GET    /api/v1/suppliers/            # List suppliers
POST   /api/v1/suppliers/            # Create supplier
GET    /api/v1/suppliers/{id}/       # Get supplier details
PUT    /api/v1/suppliers/{id}/       # Update supplier
DELETE /api/v1/suppliers/{id}/       # Delete supplier
```

### Products
```
GET    /api/v1/products/             # List products
POST   /api/v1/products/             # Create product
GET    /api/v1/products/{id}/        # Get product details
PUT    /api/v1/products/{id}/        # Update product
DELETE /api/v1/products/{id}/        # Delete product
GET    /api/v1/products/low_stock/   # Get low stock products
```

### Analytics
```
GET    /api/v1/dashboard/overview/   # Dashboard metrics
GET    /api/v1/analytics/sales/      # Sales statistics
```

### Additional Resources
```
POST   /api/v1/proforma-invoices/    # Proforma invoices
GET    /api/v1/delivery-notes/       # Delivery notes
GET    /api/v1/customer-orders/      # Customer orders
GET    /api/v1/supplier-orders/      # Supplier orders
GET    /api/v1/payments/             # Payments
```

---

## 🔐 Authentication

### Get API Token
```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Response:
{"token": "YOUR_TOKEN_HERE"}
```

### Use Token in API Requests
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://127.0.0.1:8000/api/v1/clients/
```

---

## 🎨 Frontend Features

### Dashboard
- 📈 KPI cards (Total Invoiced, Paid, Pending, Overdue)
- 📊 Sales trend chart (Last 12 months)
- ⚠️ Low stock alerts
- 📋 Recent invoices table
- 💳 Recent payments table
- 🔍 Search functionality

### Responsive Design
- ✅ Mobile-friendly layout
- ✅ Tablet optimized
- ✅ Desktop full-featured
- ✅ Dark mode ready (can be added)

---

## 💾 Data Management

### Export Features
- **PDF Export**: Professional invoice documents
- **Excel Export**: Spreadsheet format for accounting software
- **JSON Export**: Data backup and integration
- **Batch Export**: Multiple documents at once

### Data Storage
- **Database**: SQLite3 (local), PostgreSQL (production)
- **Media Files**: Product images, uploaded documents
- **Static Files**: CSS, JavaScript, images

---

## 🌐 API Filtering & Search

### Filter Examples
```bash
# Filter by status
GET /api/v1/invoices/?status=paid

# Filter by client
GET /api/v1/invoices/?client=client-uuid

# Filter by date range
GET /api/v1/invoices/?invoice_date__gte=2025-01-01&invoice_date__lte=2025-12-31
```

### Search Examples
```bash
# Search invoices
GET /api/v1/invoices/?search=INV-2025

# Search clients
GET /api/v1/clients/?search=John

# Search products
GET /api/v1/products/?search=laptop
```

### Ordering Examples
```bash
# Order by date (descending)
GET /api/v1/invoices/?ordering=-invoice_date

# Order by amount
GET /api/v1/invoices/?ordering=total
```

### Pagination
```bash
# Get second page (20 items per page default)
GET /api/v1/invoices/?page=2
```

---

## 🛡️ Security Features

- ✅ CSRF Protection
- ✅ SQL Injection Prevention (Django ORM)
- ✅ XSS Protection
- ✅ Token Authentication
- ✅ CORS Configuration
- ✅ User Role Management
- ✅ Read-only Fields for Sensitive Data
- ✅ Audit Trail (Create/Update timestamps)

---

## 📈 Dashboard Metrics

The dashboard provides:
- **Total Invoiced**: Sum of all invoice totals
- **Total Paid**: Sum of all received payments
- **Pending Invoices**: Count of unpaid invoices
- **Overdue Invoices**: Invoices past due date
- **Monthly Metrics**: Invoiced and paid amounts for current month
- **Client Statistics**: Total and new clients this month
- **Stock Alerts**: Count of low-stock products

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up SSL/HTTPS
- [ ] Configure allowed hosts
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up logging
- [ ] Configure email backend
- [ ] Set up static file serving (CDN/S3)
- [ ] Configure media file storage
- [ ] Set up backups

### Production Server Setup
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn invoice_project.wsgi:application --bind 0.0.0.0:8000
```

---

## 📞 API Response Examples

### Get Dashboard Overview
```json
{
  "total_invoices": 150000.00,
  "total_paid": 145000.00,
  "pending_invoices": 8,
  "overdue_invoices": 2,
  "month_invoiced": 25000.00,
  "month_paid": 23000.00,
  "total_clients": 45,
  "new_clients_this_month": 3,
  "low_stock_products": 5
}
```

### Get Invoices List
```json
{
  "count": 120,
  "next": "http://127.0.0.1:8000/api/v1/invoices/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "invoice_number": "INV-2025-001",
      "client": "uuid-here",
      "client_name": "Acme Corp",
      "invoice_date": "2025-12-22",
      "due_date": "2026-01-22",
      "status": "paid",
      "subtotal": 5000.00,
      "tax_amount": 1000.00,
      "total": 6000.00,
      "paid_amount": 6000.00,
      "items": [
        {
          "description": "Product Name",
          "quantity": 2.0,
          "unit_price": 2500.00,
          "tax_rate": 20.0,
          "total": 6000.00
        }
      ]
    }
  ]
}
```

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check for errors
python manage.py check

# Make sure migrations are applied
python manage.py migrate

# Create superuser if needed
python manage.py createsuperuser
```

### Database issues
```bash
# Reset database (development only!)
# 1. Delete db.sqlite3
# 2. Run migrations again
python manage.py migrate
```

### Import errors
```bash
# Ensure virtual environment is activated
# Reinstall packages
pip install -r requirements.txt
```

### API not responding
```bash
# Check if server is running
# Check CORS settings in settings.py
# Verify authentication token format
```

---

## 📚 Documentation

### For Developers
- See `PROJECT_SETUP.md` for detailed technical documentation
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- ReportLab: https://www.reportlab.com/docs/

### For Users
- Invoice templates available in `/templates/`
- Sample data loading instructions
- User role and permission guidelines

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 💬 Support

For issues, questions, or feature requests:
1. Check the PROJECT_SETUP.md documentation
2. Review API endpoint examples above
3. Check Django and DRF documentation
4. Test using the admin interface first

---

## 🎉 Features Summary

### ✅ Completed
- 16+ Database models with relationships
- Complete REST API with 50+ endpoints
- Django admin interface with custom configurations
- PDF & Excel export functionality
- Advanced filtering and search
- Token authentication
- User roles and permissions
- Dashboard analytics
- Professional HTML template with Tailwind CSS
- Comprehensive documentation

### ⏳ Ready for Frontend
- Invoice management interface
- Client management interface
- Product catalog interface
- Payment tracking interface
- Report generation
- Mobile app (optional)

---

## 📊 Project Statistics

- **Models**: 16 custom models
- **API Endpoints**: 50+
- **Admin Pages**: 10
- **User Roles**: 4
- **Document Types**: 5
- **Export Formats**: 2 (PDF, Excel)
- **Languages**: 2 (French, English)
- **Response Types**: JSON
- **Authentication**: Token-based
- **Database**: SQLite3/PostgreSQL-ready

---

**Version**: 1.0.0  
**Last Updated**: December 22, 2025  
**Status**: Production Ready (Backend), Frontend Ready for Implementation  
**Python**: 3.11+  
**Django**: 6.0  

---

Enjoy your professional invoice management system! 🚀
