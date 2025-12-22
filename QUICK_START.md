# 🚀 Quick Start Guide - Invoice Management System

## 5-Minute Setup

### 1️⃣ Activate Virtual Environment (30 seconds)

**Windows:**
```bash
cd "g:\Training de formations Udemy\Modern HTML-CSS"
invoice_env\Scripts\activate
```

**Linux/Mac:**
```bash
cd "path/to/project"
source invoice_env/bin/activate
```

✅ You should see `(invoice_env)` in your command prompt.

---

### 2️⃣ Start Django Server (30 seconds)

```bash
python manage.py runserver
```

**Output should show:**
```
Starting development server at http://127.0.0.1:8000/
```

✅ Server is running!

---

### 3️⃣ Access the Application (30 seconds)

Open your browser and navigate to:

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/admin/ | Admin Dashboard |
| http://127.0.0.1:8000/api/v1/ | API Browsable Interface |
| http://127.0.0.1:8000/api-token-auth/ | Get API Token |

---

### 4️⃣ Login to Admin

1. Go to http://127.0.0.1:8000/admin/
2. Username: `admin` (or your superuser username)
3. Password: (your superuser password)

**First time login?** Create a superuser:
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

---

### 5️⃣ Get API Token (1 minute)

#### Using curl:
```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

#### Using Postman:
1. Method: `POST`
2. URL: `http://127.0.0.1:8000/api-token-auth/`
3. Body (JSON):
```json
{
  "username": "admin",
  "password": "your_password"
}
```

#### Response:
```json
{
  "token": "abcdef123456...your_token..."
}
```

✅ Copy your token - you'll use it for API requests.

---

## API Quick Reference

### List Invoices
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/invoices/
```

### List Clients
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/clients/
```

### List Products
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/products/
```

### Get Dashboard Metrics
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/dashboard/overview/
```

---

## Admin Panel Quick Tour

### 📋 Managing Invoices

1. Go to Admin → **Invoices**
2. Click **Add Invoice**
3. Fill in:
   - Invoice Number: `INV-2025-001`
   - Client: Select from dropdown
   - Invoice Date & Due Date
   - Status: Select status
4. Click **Add another Invoice Item** to add products
5. Click **Save**

### 👥 Managing Clients

1. Go to Admin → **Clients**
2. Click **Add Client**
3. Fill in:
   - Name, Company
   - Email, Phone, Address
   - Tax ID, Credit Limit
4. Click **Save**

### 📦 Managing Products

1. Go to Admin → **Products**
2. Click **Add Product**
3. Fill in:
   - Name, SKU, Reference
   - Unit Price, Cost Price
   - Tax Rate, Category
   - Stock Level, Reorder Level
4. Click **Save**

### 💳 Recording Payments

1. Go to Admin → **Payments**
2. Click **Add Payment**
3. Select Invoice
4. Enter:
   - Payment Date
   - Amount
   - Payment Method
   - Reference Number
5. Click **Save**

---

## Data Entry Workflow

### Step 1: Create a Client
Admin → Clients → Add Client → Fill details → Save

### Step 2: Create Products (if needed)
Admin → Products → Add Product → Fill details → Save

### Step 3: Create an Invoice
Admin → Invoices → Add Invoice
- Select client
- Add line items (products)
- Set status to "draft"
- Save

### Step 4: Send Invoice
Update invoice status to "sent"

### Step 5: Record Payment
Admin → Payments → Add Payment
- Select invoice
- Enter payment details
- Save

### Step 6: Mark Paid
Update invoice status to "paid"

---

## Exporting Documents

### From Admin Interface
1. Open Invoice
2. Look for export buttons (if frontend is implemented)
3. Choose PDF or Excel format
4. File downloads

### From API
```bash
# Export as PDF
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/invoices/INVOICE_UUID/export_pdf/

# Export as Excel  
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/invoices/INVOICE_UUID/export_excel/

# Export all invoices
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/invoices/export_all_excel/
```

---

## Common Tasks

### ❓ How to find an invoice?

**In Admin:**
1. Go to Invoices
2. Use search box: Search for invoice number or client name
3. Use Status filter: Select "Paid", "Overdue", etc.

**Via API:**
```bash
curl "http://127.0.0.1:8000/api/v1/invoices/?search=INV-2025&status=paid" \
  -H "Authorization: Token YOUR_TOKEN"
```

### ❓ How to see low stock products?

**In Admin:**
1. Go to Products
2. Look for products with red "Low Stock" indicator

**Via API:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/products/low_stock/
```

### ❓ How to check dashboard metrics?

**Via API:**
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/v1/dashboard/overview/
```

Response shows:
- Total invoiced amount
- Total paid amount
- Number of pending invoices
- Number of overdue invoices
- Monthly metrics
- Low stock products count

### ❓ How to filter invoices by date?

**In Admin:**
1. Go to Invoices
2. Click "Filter" on right side
3. Click "By Invoice Date"
4. Select date range

**Via API:**
```bash
curl "http://127.0.0.1:8000/api/v1/invoices/?invoice_date__gte=2025-01-01&invoice_date__lte=2025-12-31" \
  -H "Authorization: Token YOUR_TOKEN"
```

---

## Useful Django Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Apply migrations
python manage.py migrate

# Create migrations (after model changes)
python manage.py makemigrations

# Run Django shell
python manage.py shell

# Reset database (WARNING: deletes all data!)
# 1. Delete db.sqlite3
# 2. python manage.py migrate

# Clear cache
python manage.py clear_cache

# Show statistics
python manage.py dbshell
```

---

## Keyboard Shortcuts

### In Admin
- `Alt + N` - Add new item
- `Alt + S` - Save
- `Tab` - Navigate fields
- `Shift + Tab` - Navigate backwards

### In Admin Search
- `/` - Focus search
- `?` - Show available shortcuts

---

## File Locations

| Item | Location |
|------|----------|
| Database | `db.sqlite3` |
| Media Files | `media/` |
| Static Files | `static/` |
| Templates | `templates/` |
| Models | `core/models.py` |
| Admin Config | `core/admin.py` |
| API Views | `api/views.py` |
| API Serializers | `api/serializers.py` |

---

## Troubleshooting

### ❌ "Port already in use"
```bash
# Use different port
python manage.py runserver 8001
```

### ❌ "ModuleNotFoundError"
```bash
# Make sure venv is activated
# Reinstall requirements
pip install -r requirements.txt
```

### ❌ "Database locked"
```bash
# Delete db.sqlite3 and restart
python manage.py migrate
python manage.py createsuperuser
```

### ❌ "Cannot connect to API"
```bash
# Check server is running
# Check token is correct
# Check Authorization header format: "Token YOUR_TOKEN"
```

---

## Next Steps

1. **Add Sample Data**
   - Create a few test clients
   - Add products
   - Create sample invoices

2. **Explore API**
   - Use Postman or curl
   - Test different endpoints
   - Try filtering and searching

3. **Build Frontend** (Optional)
   - Create forms for data entry
   - Build dashboard
   - Implement export buttons

4. **Setup Production** (When Ready)
   - Change DEBUG to False
   - Configure PostgreSQL database
   - Setup web server (Gunicorn)
   - Configure SSL/HTTPS

---

## Documentation Links

- **Full README**: See `README.md`
- **Setup Details**: See `PROJECT_SETUP.md`
- **API Documentation**: See `API_DOCUMENTATION.md`
- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/

---

## Support

If you encounter issues:
1. Check the documentation files
2. Review error messages carefully
3. Check Django logs (`python manage.py check`)
4. Try resetting the database
5. Reinstall requirements

---

## Success Checklist ✅

- [ ] Virtual environment activated
- [ ] Django server running
- [ ] Admin page accessible
- [ ] API token obtained
- [ ] Can list invoices via API
- [ ] Can create a client
- [ ] Can create an invoice
- [ ] Can export to PDF/Excel

**Once all checked, you're ready to use the system!** 🎉

---

**Happy invoicing!** 📊💼
