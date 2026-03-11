from apps.home.models import AuditLog
from django.shortcuts import render
from django.core.paginator import Paginator

def audit_log_list(request):

    page_number = request.GET.get("page", 1)
    per_page = 20
    keyword = request.GET.get("keyword", "")
    column = request.GET.get("column", "")

    columns = [
        field.name
        for field in AuditLog._meta.fields
        if field.name not in ['id', 'object_id']
    ]

    qs = AuditLog.objects.all().order_by("-created_at")

    if column.lower() == "user":
        qs = qs.filter(**{f"user__username__icontains": keyword})
    elif column and keyword:
        qs = qs.filter(**{f"{column}__icontains": keyword})

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)
    

    return render(request, "home/audit-log.html", 
                  {
                    "logs": page_obj,
                    "paginator": paginator,
                    "keyword": keyword,
                    "columns": columns
                  })
