from apps.home.models import AuditLog

def log_audit(request, action, instance, before=None, after=None):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        model=instance.__class__.__name__,
        object_id=instance.pk,
        endpoint=request.path,
        http_method=request.method,
        before=before,
        after=after,
    )
    
    
