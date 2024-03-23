from .models import ProfileData
from .constants import *

def icon(request):
    if request.user.is_authenticated:
        user_profile = ProfileData.objects.filter(user_id=request.user.id)
        if user_profile[0].icon == None:
            user_profile[0].icon = DEFAULT_ARTIST_IMAGE
        return { 'icon': user_profile[0].icon }
    else:
        user_profile = None
        return { 'icon': user_profile }
