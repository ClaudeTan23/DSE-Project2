from django.urls import path, re_path
from apps.home import views
from apps.home.views import index, products, reports, stock, audit_views, sale, alert_notification
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(index.dashboard, login_url="/login/"), name='home'),
    path('products/add/', login_required(products.add_product, login_url="/login/"), name='add_product'),
    path('products/update/<int:product_id>/', login_required(products.product_update, login_url="/login/"), name='update_product'),
    path('products/delete/<int:product_id>/', login_required(products.product_delete, login_url="/login/"), name='delete_product'),
    path("products", login_required(products.fetch_products , login_url="/login/"), name="fetch_products"),
    path("reports", login_required(reports.report_page, login_url="/login/"), name="report_page"),
    path("reports/fetch/", login_required(reports.fetch_stock_report , login_url="/login/"), name="fetch_stock_report"),
    path("stock", login_required(stock.home, login_url="/login/"), name="stock_page"),
    path("stock/in", login_required(stock.stock_in, login_url="/login/"), name="stock_in"),
    path("stock/out", login_required(stock.stock_out, login_url="/login/"), name="stock_out"),
    path("audit", login_required(audit_views.audit_log_list, login_url="/login/"), name="audit_log"),
    path("sales", login_required(sale.sales, login_url="/login/"), name="sales"),
    path("sales/create/", login_required(sale.create_sales, login_url="/login/"), name="create_sale"),
    path("alerts/low-stock/", login_required(alert_notification.low_stock_alert, login_url="/login/"), name="alert_low_stock"),

    # Matches any html file
    re_path(r'^.*\.*', index.pages, name='pages'),

]
