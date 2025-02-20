import tempfile

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from weasyprint import HTML
from cffi import FFI

import os
import ctypes

# Check if the library exists
lib_path = "C:/msys64/ucrt64/bin/libgobject-2.0-0.dll"
if os.path.exists(lib_path):
    print("Library found.")
    try:
        ctypes.CDLL(lib_path)
        print("Library loaded successfully.")
    except Exception as e:
        print(f"Error loading library: {e}")
else:
    print("Library not found.")


def generate_purchase_order_pdf(po_number):
    # Fetch the purchase order from the database
    purchase_order = get_object_or_404(PurchaseOrder, po_number=po_number)

    # Fetch purchase order items
    items = PurchaseOrderItem.objects.select_related(
        "purchase_order", "product", "approved_by"
    ).filter(purchase_order=purchase_order)

    # Prepare dynamic context
    context = {
        # Header Section
        "po_number": purchase_order.po_number,
        "date": purchase_order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "qtn_ref": purchase_order.qtn_ref,  # Add QTN Ref
        # PO Issued To Section
        "vendor_name": purchase_order.vendor.name,
        "vendor_address": purchase_order.vendor.address,
        "vendor_phone": purchase_order.vendor.phone,
        "vendor_email": purchase_order.vendor.email,
        # Bill To Section
        "bill_to_name": purchase_order.bill_to_name,  # Add Bill To Name
        "bill_to_address": purchase_order.bill_to_address,  # Add Bill To Address
        "bill_to_phone": purchase_order.bill_to_phone,  # Add Bill To Phone
        # Subject Section
        "subject": purchase_order.subject,  # Add Subject
        "subject_description": purchase_order.subject_description,  # Add Subject Description
        # Order Details Section
        "items": [
            {
                "name": item.product.name,
                "uom": item.product.uom,  # Add UOM
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price,
            }
            for item in items
        ],
        # Totals Section
        "sub_total": purchase_order.sub_total,  # Add Sub-Total
        "vat": purchase_order.vat,  # Add VAT
        "grand_total": purchase_order.grand_total,  # Add Grand Total
        "total_price": purchase_order.total_price,
        "total_in_words": purchase_order.total_in_words,  # Add Total in Words
        # Terms and Conditions Section
        "terms_and_conditions": purchase_order.terms_and_conditions,  # Add Terms and Conditions
        # Payment Terms Section
        "payment_terms": purchase_order.payment_terms,  # Add Payment Terms
        # Delivery Location Section
        "delivery_location": purchase_order.delivery_location,  # Add Delivery Location
        # Footer Section
        "company_name": purchase_order.company_name,  # Add Company Name
        "company_address": purchase_order.company_address,  # Add Company Address
        "company_phone": purchase_order.company_phone,  # Add Company Phone
        "company_email": purchase_order.company_email,  # Add Company Email
        "manager_name": purchase_order.manager_name,  # Add Manager Name
        "md_name": purchase_order.md_name,  # Add Managing Director Name
    }

    # Render HTML template to string
    html_content = render_to_string("purchase_order.html", context)

    # Generate PDF
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html_content).write_pdf(pdf_file.name)

    return pdf_file.name


def send_purchase_order_email(
    purchase_order, pdf_path, to_emails=None, cc_emails=None, bcc_emails=None
):
    # Default to the vendor's email if no recipient is passed
    if not to_emails:
        to_emails = [purchase_order.vendor.email]

    # Prepare the email content
    subject = f"Purchase Order {purchase_order.po_number}"
    body = f"Dear {purchase_order.vendor.name},\n\nPlease find attached your purchase order {purchase_order.po_number}.\n\nBest Regards,\n{purchase_order.created_by.get_full_name()}"

    # Create the email object
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="istiaqhasan93@gmail.com",
        to=to_emails,  # Dynamic recipient list
        cc=cc_emails,  # Optional CC
        bcc=bcc_emails,  # Optional BCC
    )

    # Attach the PDF file to the email
    with open(pdf_path, "rb") as pdf:
        email.attach(
            f"Purchase_Order_{purchase_order.po_number}.pdf",
            pdf.read(),
            "application/pdf",
        )

    # Send the email
    email.send()
