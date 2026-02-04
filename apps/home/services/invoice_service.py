from django.db import transaction
from django.utils import timezone
from apps.home.models import SaleItem, Sale

def generate_invoice_no():
    today = timezone.now()
    prefix = today.strftime("INV-%Y%m%d-")  # INV-20260203-

    last_sale = (
        Sale.objects
        .filter(invoice_no__startswith=prefix)
        .order_by("-id")
        .first()
    )

    if last_sale:
        last_number = int(last_sale.invoice_no.split("-")[-1])
        next_number = last_number + 1
    else:
        next_number = 1

    return f"{prefix}{next_number:04d}"