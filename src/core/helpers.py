import tempfile

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from weasyprint import HTML


def generate_purchase_order_pdf(po_number):
    # Fetch the purchase order from the database
    purchase_order = get_object_or_404(PurchaseOrder, po_number=po_number)

    # Fetch purchase order items
    items = PurchaseOrderItem.objects.select_related(
    'purchase_order',  
    'product',          
    'approved_by'       
    ).filter(purchase_order=purchase_order)

    # Prepare dynamic context
    context = {
        "po_number": purchase_order.po_number,
        "date": purchase_order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "vendor_name": purchase_order.vendor.name,
        "vendor_address": purchase_order.vendor.address,
        "vendor_phone": purchase_order.vendor.phone,
        "vendor_email": purchase_order.vendor.email,
        "created_by": purchase_order.created_by.get_full_name(),
        "status": purchase_order.status,
        "items": [
            {
                "name": item.product.name,
                "description": item.product.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price,
                "approved_by": item.approved_by.get_full_name(),
                "approval_type": item.approval_type,
                "approved_at": item.approved_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for item in items
        ],
        "total_price": purchase_order.total_price,
    }

    # Render HTML template to string
    html_content = render_to_string("purchase_order.html", context)

    # Generate PDF
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html_content).write_pdf(pdf_file.name)

    return pdf_file.name



def send_purchase_order_email(purchase_order, pdf_path, to_emails=None, cc_emails=None, bcc_emails=None):
    """
    Send an email with the purchase order and its PDF to the specified recipients.

    :param purchase_order: The purchase order object containing order details.
    :param pdf_path: The path to the generated PDF file.
    :param to_emails: List of recipient email addresses (primary recipients).
    :param cc_emails: List of CC recipient email addresses (optional).
    :param bcc_emails: List of BCC recipient email addresses (optional).
    """
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
        from_email="istiaqhasan93@gmail.com",  # Change this to your email
        to=to_emails,  # Dynamic recipient list
        cc=cc_emails,  # Optional CC
        bcc=bcc_emails,  # Optional BCC
    )
    
    # Attach the PDF file to the email
    with open(pdf_path, "rb") as pdf:
        email.attach(f"Purchase_Order_{purchase_order.po_number}.pdf", pdf.read(), "application/pdf")
    
    # Send the email
    email.send()
