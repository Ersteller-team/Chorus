from django.shortcuts import render
from django.http import JsonResponse
from . import spotify_data
from .spotify_constants import *

# Create your views here.
def home(request):
    response = spotify_data.search_track_id('7KYZQay4ok85FWx1e5SweU')
    response = spotify_data.search_track_artist([SPOTIFY_SEARCH_TYPE_TRACK], 'ホムンクルス')
    response = spotify_data.search_query([SPOTIFY_SEARCH_TYPE_TRACK], 'ホムンクルス')
    return JsonResponse({ 'response': response })
