from .models import ProfileData

def icon(request):
    if request.user.is_authenticated:
        user_profile = ProfileData.objects.filter(user_id=request.user.id)
        return { 'icon': user_profile[0].icon }
    else:
        user_profile = None
        return { 'icon': user_profile }
