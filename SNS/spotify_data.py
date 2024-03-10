# ------------ Import Libraries ------------
import requests
from .spotify_token import *


# ------------ Get Recent Play Data ---------------

def get_recent_play(access_token, request, limit = 20):
    
    headers = create_header(access_token, request)
    
    params = {
        'limit': limit,
    }
    
    response = requests.get(SPOTIFY_RECENT_PLAY_URL, params=params, headers=headers).json()
    
    pick_data = pick_song_data_from_json(response, SPOTIFY_RECENT_PLAY)
    
    return pick_data


# ------------ Get Saved Track Data ---------------

def get_saved_track(access_token, request, limit = 20, offset = 0):

    headers = create_header(access_token, request)
    
    params = {
        'limit': limit,
        'offset': offset,
    }
    
    response = requests.get(SPOTIFY_SAVED_TRACKS_URL, params=params, headers=headers).json()
    
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
