from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse

def get_user_profile(request):
    user = User.objects.get(id=request.user.id)

    return render(request, "home/settings.html", {"user": user})

@require_POST
def profile_update(request):
    
    try:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return JsonResponse({
            "status": "success",
            "message": "Profile updated successfully"
        })
    
    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        })