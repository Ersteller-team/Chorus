from django.urls import path
from . import views

app_name = 'SNS'

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('song/<slug:track_id>', views.song, name='song'),
    path('post/', views.post, name='post'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('check/username/', views.username_check, name='username_check'),
    path('search/song/', views.search_song, name='search_song'),
    path('signup/', views.AccountRegistration.as_view(), name='signup'), 
    path('signin/', views.Signin, name='signin'), 
    path('signout/', views.Signout, name='signout'),
    path('csrf_token/', views.csrf_token, name='csrf_token'),
]
