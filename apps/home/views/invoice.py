from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404
from apps.home.models import Sale

def invoice_pdf(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    html_string = render_to_string("home/PDF/invoice.html", {
        "sale": sale
    })
    
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{sale.invoice_no}.pdf"'
    return response
