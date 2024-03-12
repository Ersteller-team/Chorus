from django.urls import path
from . import views

app_name = 'SNS'

urlpatterns = [
    
    # Main
    path('home/', views.home, name='home'), 
    path('search/', views.search, name='search'),
    path('search/song/<slug:track_id>', views.song, name='song'),
    path('search/album/<slug:album_id>', views.album, name='album'),
    path('search/artist/<slug:artist_id>', views.artist, name='artist'),
    path('search/playlist/<slug:playlist_id>', views.playlist, name='playlist'),
    path('post/', views.post, name='post'),
    path('post/good', views.postGood, name='postgood'),
    path('post/delete', views.postDelete, name='postdelete'),
    path('spotify', views.spotify, name='spotify'),
    path('spotify/callback', views.spotify_callback, name='spotify_callback'),
    path('profile/<slug:username>', views.profile, name='profile'),
    path('profile/<slug:username>/edit', views.profile_edit, name='profile_edit'),
    path('profile/<slug:username>/song/follow', views.user_song, name='song_follow'),
    path('profile/<slug:username>/user/follow', views.user_follow, name='user_follow'),
    path('profile/<slug:username>/user/follower', views.user_follower, name='user_follower'),
    
    # Json Response
    path('check/username/', views.username_check, name='username_check'),
    path('search/song/', views.search_song, name='search_song'),
    path('search/any/', views.search_any, name='search_any'),
    
    # Account
    path('signup/', views.AccountRegistration.as_view(), name='signup'), 
    path('signin/', views.Signin, name='signin'), 
    path('signout/', views.Signout, name='signout'),
    
    # CSRF Token
    path('csrf_token/', views.csrf_token, name='csrf_token'),
    
]
