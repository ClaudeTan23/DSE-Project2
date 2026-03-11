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
from apps.home.utils.audit import log_audit
from apps.home.utils.json import make_json_safe
from django.forms.models import model_to_dict


def sales(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    
    return render(request, 'home/sale.html', context)

from django.db import transaction
from django.http import JsonResponse
import json

@require_POST
@transaction.atomic
def create_sales(request):
    try:
        data = json.loads(request.body)

        payment_method = data.get("payment_method")
        items = data.get("items", [])

        if not items:
            raise ValueError("No sale items provided")

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
                raise ValueError(f"Insufficient stock for {product.name}")
            
            old_data_product = make_json_safe(model_to_dict(product))

            line_total = product.price * qty
            total += line_total

            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=qty,
                unit_price=product.price,
                line_total=line_total
            )

            product.stock -= qty
            product.save()

            log_audit(
                request=request,
                action="UPDATE",
                instance=product,
                before=old_data_product,
                after=make_json_safe(model_to_dict(product))
            )
            

            createStock = Stock.objects.create(
                product=product,
                quantity=qty,
                transaction_type="OUT",
                location="Sales",
                reference_type="SALE",
                reference_id=sale.id
            )

            log_audit(
            request=request,
            action="CREATE",
            instance=createStock,
            after=make_json_safe(model_to_dict(createStock))
        )

        sale.total_amount = total
        sale.save()

        log_audit(
            request=request,
            action="CREATE",
            instance=sale,
            after=make_json_safe(model_to_dict(sale))
        )

        return JsonResponse({
            "success": True,
            "invoice_no": invoice_no,
            "total": float(total)
        })

    except Exception as e:
        transaction.set_rollback(True)

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


def sales_list(request):
    page_number = request.GET.get("page", 1)
    keyword = request.GET.get("keyword", "")
    column = request.GET.get("column", "")
    per_page = 20

    qs = Sale.objects.order_by("-sale_date")

    columns = [
        field.name
        for field in Sale._meta.fields
        if field.name not in ['id']
    ]


    if column.lower() == "user":
        qs = qs.filter(**{f"user__username__icontains": keyword})
        
    elif column and keyword:
        qs = qs.filter(**{f"{column}__icontains": keyword})

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home/sales.html",
        {
            "sales": page_obj,
            "paginator": paginator,
            "keyword": keyword,
            "columns": columns
        }
    )
