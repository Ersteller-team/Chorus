# ------------ Import Libraries ------------
import requests
import base64
from .spotify_secret import *
from .constants import *
from .spotify_pick_data import *


# ------------ Get Authenticate URL ---------------

def get_authenticate_url():
    
    auth_url = SPOTIFY_AUTHENTICATION_URL + '?client_id=' + SPOTIFY_CLIENT_ID + '&response_type=code&redirect_uri=' + SPOTIFY_REDIRECT_URI + '&show_dialog=true&scope=' + SPOTIFY_AUTHENTICATE_SCOPE
    
    return auth_url


# ------------ Create header ---------------

def create_header(access_token = None):
    
    if access_token == None:
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        }
        
        token_response = requests.post(SPOTIFY_TOKEN_URL, data=data).json()
        
        access_token = token_response['access_token']
    
    response = {
        'Authorization': f'Bearer {access_token}',
        'Accept-Language': 'ja',
    }
    
    return response


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
    refresh_token = token_response['refresh_token']
    
    return access_token, refresh_token


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


# ------------ Get Saved Track Data ---------------

def get_saved_track(access_token, limit = 20, offset = 0):

    headers = create_header(access_token)
    
    params = {
        'limit': limit,
        'offset': offset,
    }
    
    response = requests.get(SPOTIFY_SAVED_TRACKS_URL, params=params, headers=headers).json()
    # return response
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_SAVED_TRACKS)
    
    return pick_data


# ------------ Search for Query ---------------

def search_query(type, query, limit = 20, offset = 0):

    headers = create_header()
    
    search_params = {
        'q': query,
        'type': type,
        'limit': limit,
        'offset': offset,
    }
    
    response = requests.get(SPOTIFY_SEARCH_TEXT_URL, params=search_params, headers=headers).json()
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_SEARCH_FOR_ITEM)
    
    return pick_data


# ------------ Search for Track & Artist ---------------

def search_track_artist(type, track = None, artist = None, limit = 20, offset = 0):
    
    query = ""
    
    if artist != None:
        query = 'artist:' + artist + ' '
    
    if track != None:
        query += 'track:' + track
    
    return search_query(type, query, limit, offset)


# ------------ Search for Track by ID ---------------

def search_track_id(track_id):

    headers = create_header()
    
    response = requests.get(SPOTIFY_SEARCH_TRACK_ID_URL + track_id, headers=headers).json()
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_GET_TRACK)
    
    return pick_data
