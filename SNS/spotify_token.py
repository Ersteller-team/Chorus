# ------------ Import Libraries ------------
import requests
import base64
from .spotify_secret import *
from .spotify_convert import *
from .models import *


# ------------ Get Authenticate URL ---------------

def get_authenticate_url():
    
    auth_url = SPOTIFY_AUTHENTICATION_URL + '?client_id=' + SPOTIFY_CLIENT_ID + '&response_type=code&redirect_uri=' + SPOTIFY_REDIRECT_URI + '&show_dialog=true&scope=' + SPOTIFY_AUTHENTICATE_SCOPE
    
    return auth_url


# ------------ Refresh Access Token ---------------

def refresh_access_token(refresh_token):
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    
    authentication = base64.b64encode((SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode())
    
    headers = {
        'Authorization': 'Basic ' + str(authentication).split("'")[1],
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    token_response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers).json()
    
    access_token = token_response['access_token']
    
    return access_token


# ------------ Create header ---------------

def create_header(access_token = None, request = None, lang='ja'):
    
    if access_token == None:
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }
        
        token_response = requests.post(SPOTIFY_TOKEN_URL, data=data).json()
        
        access_token = token_response['access_token']
    
    else:
        
        response = {
            'Authorization': f'Bearer {access_token}',
            'Accept-Language': 'ja',
        }
        
        params = {
            'limit': 1,
        }
        
        test_token = requests.get(SPOTIFY_SAVED_TRACKS_URL, params=params, headers=response).json()
        
        if 'error' in test_token:
            
            user = ProfileData.objects.get(user_id = request.user.id)
            
            access_token = refresh_access_token(user.spotify_refresh_token)
            
            user.spotify_access_token = access_token
            user.save()
    
    response = {
        'Authorization': f'Bearer {access_token}',
    }
    
    if lang == 'ja':
        
        response['Accept-Language'] = 'ja'
    
    return response


# ------------ Get Access Token ---------------

def get_access_token_authentication(code):
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
    }
    
    authentication = base64.b64encode((SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode())
    
    headers = {
        'Authorization': 'Basic ' + str(authentication).split("'")[1],
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    token_response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers).json()
    
    access_token = token_response['access_token']
    
    refresh_token = token_response['refresh_token']
    
    return access_token, refresh_token