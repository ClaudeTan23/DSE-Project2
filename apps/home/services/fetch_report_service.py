from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from ..models import Stock
from django.core.paginator import Paginator
import json


def get_report_data(
    period="daily",
    product_id=None,
    date_from=None,
    date_to=None
):
    qs = Stock.objects.all()

    if product_id:
        qs = qs.filter(product_id=product_id)

    if date_from:
        qs = qs.filter(last_updated__date__gte=date_from)

    if date_to:
        qs = qs.filter(last_updated__date__lte=date_to)

    # Time grouping
    if period == "weekly":
        qs = qs.annotate(time=TruncWeek("last_updated"))
    elif period == "monthly":
        qs = qs.annotate(time=TruncMonth("last_updated"))
    elif period == "yearly":
        qs = qs.annotate(time=TruncYear("last_updated"))
    else:
        qs = qs.annotate(time=TruncDate("last_updated"))

    data = (
        qs.values("time", "transaction_type", "reference_type")
          .annotate(total=Sum("quantity"))
          .order_by("time")
    )

    result = {}

    for row in data:
        # Label formatting
        if period == "yearly":
            key = row["time"].strftime("%Y")
        elif period == "monthly":
            key = row["time"].strftime("%Y-%m")
        else:
            key = row["time"].strftime("%Y-%m-%d")

        if key not in result:
            result[key] = {
                "IN": 0,
                "OUT": 0,
                "SALE": 0
            }

        # IN stock
        if row["transaction_type"] == "IN":
            result[key]["IN"] += row["total"]

        # SALE (OUT + reference)
        elif row["transaction_type"] == "OUT" and row["reference_type"] == "SALE":
            result[key]["SALE"] += row["total"]
            result[key]["OUT"] += row["total"]

        # Normal OUT (adjustment / damage / transfer)
        elif row["transaction_type"] == "OUT":
            result[key]["OUT"] += row["total"]
 
    return result



def get_report_table_data(product_id=None, date_from=None, date_to=None, page_number=None):
    qs = Stock.objects.select_related("product")
    per_page = 20

    if product_id:
        qs = qs.filter(product_id=product_id)

    if date_from:
        qs = qs.filter(last_updated__date__gte=date_from)

    if date_to:
        qs = qs.filter(last_updated__date__lte=date_to)

    qs = qs.order_by("-last_updated")
    
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "date": s.last_updated.strftime("%Y-%m-%d %H:%M"),
            "product": s.product.name,
            "type": s.transaction_type,
            "quantity": s.quantity,
            "location": s.location,
            "IsSale": s.reference_type == "SALE"
        }
        for s in page_obj
    ]
    
    return data, paginator, page_obj

def get_all_report_table_excel(product_id=None, date_from=None, date_to=None, page_number=None):
    qs = Stock.objects.select_related("product")

    if product_id:
        qs = qs.filter(product_id=product_id)

    if date_from:
        qs = qs.filter(last_updated__date__gte=date_from)

    if date_to:
        qs = qs.filter(last_updated__date__lte=date_to)

    data = [
        {
            "Product": s.product.name,
            "Last Update": s.last_updated.strftime("%Y-%m-%d %H:%M"),
            "Transaction Type": s.transaction_type,
            "Quantity": s.quantity,
            "Location": s.location,
            "FromSale": s.reference_type == "SALE"
        }
        for s in qs
    ]
    
    return data
    
