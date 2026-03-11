from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from apps.home.models import Product, Sale
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
import logging
from django.db.models import Sum

def dashboard(request):
    products = Product.objects.all()

    today = timezone.now().date()

    today_total_sales = Sale.objects.filter(
        sale_date__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    total_stock = products.aggregate(total=Sum('stock'))
    out_of_stock = products.filter(stock=0).count()

    labels = [p.name for p in products]
    quantities = [p.stock for p in products]

    context = {
        'labels': labels,
        'quantities': quantities,
        'totalStock': total_stock,
        'total_outStock': out_of_stock,
        'totalSale': today_total_sales
    }
    
    logger = logging.getLogger("core")
    logger.debug("TEST")
    
    return render(request, 'home/dashboard.html', context)


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

