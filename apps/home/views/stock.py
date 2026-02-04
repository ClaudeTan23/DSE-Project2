from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render
from apps.home.models import Product, Stock, AuditLog
from apps.home.utils.audit import log_audit
from apps.home.utils.json import make_json_safe
from django.forms.models import model_to_dict


def home(request):
    products = Product.objects.all().order_by('-created_at')

    context = {
        "products": products
    }
    
    return render(request, 'home/stock.html', context)

@transaction.atomic
def stock_in(request):
    if request.method != "POST":
        return redirect("stock_page")

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 0))
    location = request.POST.get("location", "Main Store")

    if quantity <= 0:
        messages.error(request, "Quantity must be greater than 0")
        return redirect("stock_page")

    product = get_object_or_404(Product, id=product_id)

    before_data = make_json_safe(model_to_dict(product))

    # Update current stock
    product.stock += quantity
    product.save()

    # Create stock transaction record
    Stock.objects.create(
        product=product,
        quantity=quantity,
        location=location,
        transaction_type="IN"
    )

    # Audit log
    log_audit(
        request=request,
        action="UPDATE",
        instance=product,
        before=before_data,
        after=make_json_safe(model_to_dict(product))
    )

    messages.success(request, "Stock added successfully")
    return redirect("stock_page")



@transaction.atomic
def stock_out(request):
    if request.method != "POST":
        return redirect("stock_page")

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 0))
    location = request.POST.get("location", "Main Store")

    if quantity <= 0:
        messages.error(request, "Quantity must be greater than 0")
        return redirect("stock_page")

    product = get_object_or_404(Product, id=product_id)

    if product.stock < quantity:
        messages.error(request, "Insufficient stock")
        return redirect("stock_page")

    before_data = make_json_safe(model_to_dict(product))

    # Deduct stock
    product.stock -= quantity
    product.save()

    # Record transaction
    Stock.objects.create(
        product=product,
        quantity=quantity,
        location=location,
        transaction_type="OUT"
    )

    # Audit log
    log_audit(
        request=request,
        action="UPDATE",
        instance=product,
        before=before_data,
        after=make_json_safe(model_to_dict(product))
    )

    messages.success(request, "Stock deducted successfully")
    return redirect("stock_page")