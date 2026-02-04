from apps.home.models import AuditLog
from django.shortcuts import render

def audit_log_list(request):
    logs = AuditLog.objects.select_related("user").order_by("-created_at")
    return render(request, "home/audit-log.html", {"logs": logs})
