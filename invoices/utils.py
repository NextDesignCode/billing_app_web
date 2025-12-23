# invoices/utils.py - Fonctions d'export
# ============================================================================
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook

def generate_invoice_pdf(invoice):
    """Generate PDF for an invoice"""
    buffer = BytesIO()
    # ... (code PDF du fichier api/exports.py)
    return buffer

def generate_invoice_excel(invoice):
    """Generate Excel for an invoice"""
    buffer = BytesIO()
    # ... (code Excel du fichier api/exports.py)
    return buffer
