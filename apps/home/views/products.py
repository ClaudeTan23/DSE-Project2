from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from apps.home.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from apps.home.utils.audit import log_audit
from apps.home.utils.json import make_json_safe
from django.forms.models import model_to_dict

@require_POST
def add_product(request):
    try:
        data = json.loads(request.body)

        product = Product.objects.create(
            name=data.get('name'),
            sku=data.get('sku'),
            category=data.get('category'),
            price=data.get('price'),
            stock=data.get('stock', 0),
            status=data.get('status', 'active'),
            description=data.get('description', '')
        )
        
        after_data = make_json_safe(model_to_dict(product))
        
        log_audit(
            request=request,
            action="CREATE",
            instance=product,
            after=after_data
        )

        return JsonResponse({
            'success': True,
            'message': 'Product added successfully',
            'product_id': product.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
        
@require_GET
def fetch_products(request):    
    page_number = request.GET.get("page", 1)
    per_page = 20

    qs = Product.objects.order_by('-created_at')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "home/products.html",
        {
            "products": page_obj,
            "paginator": paginator,
        }
    )


def product_update(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)

        before_data = make_json_safe(model_to_dict(product))
        data = json.loads(request.body)

        product.name = data.get("name")
        product.sku = data.get("sku")
        product.category = data.get("category")
        product.price = data.get("price")
        product.stock = data.get("stock")
        product.save()

        after_data = make_json_safe(model_to_dict(product))

        log_audit(
            request=request,
            action="UPDATE",
            instance=product,
            before=before_data,
            after=after_data
        )

    return JsonResponse({"success": True})


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    before_data = make_json_safe(model_to_dict(product))

    log_audit(
        request=request,
        action="DELETE",
        instance=product,
        before=before_data
    )

    product.delete()
    return JsonResponse({"success": True})