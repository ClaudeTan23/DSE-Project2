from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request):
    products = Product.objects.all()

    labels = [p.name for p in products]
    quantities = [p.quantity for p in products]

    context = {
        'labels': labels,
        'quantities': quantities,
    }
    return render(request, 'dashboard.html', context)

@login_required
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
    products = Product.objects.all().order_by('-created_at')

    context = {
        "products": products
    }

    return render(request, "home/products.html", context)