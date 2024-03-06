from django.shortcuts import render
from django.http import JsonResponse
from . import spotify_data
from .spotify_constants import *

# Create your views here.
def home(request):
    response = spotify_data.search_query([SPOTIFY_SEARCH_TYPE_TRACK], 'Lemon 米津玄師')
    return JsonResponse({ 'response': response })
