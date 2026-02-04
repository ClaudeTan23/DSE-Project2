from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.home.models import Product


@require_GET
def low_stock_alert(request):

    threshold = int(request.GET.get("threshold", 105)) # stock limit

    products = (
        Product.objects
        .filter(stock__lte=threshold, status="active")
        .order_by("stock")
    )

    data = [
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "stock": p.stock,
        }
        for p in products
    ]

    return JsonResponse({
        "count": len(data),
        "threshold": threshold,
        "products": data
    })
