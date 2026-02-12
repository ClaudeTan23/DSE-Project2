from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from decimal import Decimal
from apps.home.models import Sale, SaleItem, Product, Stock
from apps.home.services import invoice_service
import json

def sales(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    
    
    return render(request, 'home/sale.html', context)

@require_POST
@transaction.atomic
def create_sales(request):
    data = json.loads(request.body)

    payment_method = data.get("payment_method")
    items = data.get("items", [])

    if not items:
        return JsonResponse({
            "success": False,
            "message": "No sale items provided"
        })

    invoice_no = invoice_service.generate_invoice_no()

    sale = Sale.objects.create(
        invoice_no=invoice_no,
        user=request.user,
        payment_method=payment_method,
        total_amount=0
    )

    total = 0

    for item in items:
        product_id = item["product_id"]
        qty = int(item["quantity"])

        product = Product.objects.select_for_update().get(id=product_id)

        if product.stock < qty:
            return JsonResponse({
                "success": False,
                "message": f"Insufficient stock for {product.name}"
            })

        line_total = product.price * qty
        total += line_total

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=qty,
            unit_price=product.price,
            line_total=line_total
        )

        # Deduct stock
        product.stock -= qty
        product.save()

        # Stock movement log
        Stock.objects.create(
            product=product,
            quantity=qty,
            transaction_type="OUT",
            location="Sales",
            reference_type="SALE",
            reference_id=sale.id
        )

    sale.total_amount = total
    sale.save()

    return JsonResponse({
        "success": True,
        "invoice_no": invoice_no,
        "total": float(total)
    })


def sales_list(request):
    page_number = request.GET.get("page", 1)
    per_page = 20

    qs = Sale.objects.order_by("-sale_date")

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home/sales.html",
        {
            "sales": page_obj,
            "paginator": paginator,
        }
    )
