from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from apps.home.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils.timezone import now
from apps.home.services.fetch_report_service import get_report_data, get_report_table_data, get_all_report_table_excel
from apps.home.services.export_excel_service import export
from django.core.paginator import Paginator


@require_GET
def report_page(request):
    products = Product.objects.all().order_by('-created_at')

    context = {
        "products": products
    }
    
    return render(request, "home/reports.html", context)


@require_GET
def fetch_stock_report(request):
    period = request.GET.get("period", "daily")
    product_id = request.GET.get("product_id")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    
    page_number = request.GET.get("page", 1)
        
    chart_data = get_report_data(
        product_id=product_id,
        period=period,
        date_from=date_from,
        date_to=date_to
    )

    table_data, paginator, page_obj = get_report_table_data(
        product_id=product_id,
        date_from=date_from,
        date_to=date_to,
        page_number=page_number
    )
    
    labels, stock_in, stock_out, stock_sale = [], [], [], []
    
    for key in chart_data:
        labels.append(key)
        stock_in.append(chart_data[key]["IN"])
        stock_out.append(chart_data[key]["OUT"])
        stock_sale.append(chart_data[key]["SALE"])

    return JsonResponse({
        "chart": {
            "labels": labels,
            "IN": stock_in,
            "OUT": stock_out,
            "SALE": stock_sale
        },
        "table": table_data,
        "paginator": {
            "page": page_obj.number,
            "page_size": paginator.per_page,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "start_index": page_obj.start_index(),
            "end_index": page_obj.end_index(),
            "page_range": list(paginator.page_range)
            }
        })
    
@require_GET
def export_excel_report(request):
    period = request.GET.get("period", "daily")
    product_id = request.GET.get("product_id")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    
    data = get_all_report_table_excel(
        product_id=product_id,
        date_from=date_from,
        date_to=date_to,
    )
    
    return export(data)