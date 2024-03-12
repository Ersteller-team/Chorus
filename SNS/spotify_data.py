# ------------ Import Libraries ------------
import requests
from .spotify_token import *


# Need User Data

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


# No Need User Data

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
    # return response
    
    pick_data = pick_any_data_from_json(response)
    
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


# ------------ Get Album Data by ID ---------------

def search_album_id(album_id):

    headers = create_header()
    
    params = {
        'limit': 50,
    }
    
    album_response = requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id, params=params, headers=headers).json()
    
    get_tracks = album_response['total_tracks']
    
    track_response = requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id + '/tracks', params=params, headers=headers).json()
    
    while len(track_response['items']) < get_tracks:
        
        track_params = {
            'limit': '50',
            'offset': len(track_response['items']),
        }
        
        track_response['items'] += requests.get(SPOTIFY_SEARCH_ALBUM_ID_URL + album_id + '/tracks', params=track_params, headers=headers).json()['items']
    
    pick_data = pick_album_data_from_json(album_response, track_response)
    
    return pick_data


# ------------ Get Artist Data by ID ---------------

def search_artist_id(artist_id):

    headers = create_header()
    
    artist_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id, headers=headers).json()
    
    track_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/top-tracks', headers=headers).json()
    
    params = {
        'include_groups': 'album,single,appears_on,compilation',
        'limit': 50,
    }
    
    album_response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/albums', params=params, headers=headers).json()
    
    while album_response['next'] != None:
        
        params = {
            'include_groups': 'album,single,appears_on,compilation',
            'limit': 50,
            'offset': len(album_response['items']),
        }
        
        response = requests.get(SPOTIFY_SEARCH_ARTIST_ID_URL + artist_id + '/albums', params=params, headers=headers).json()
        
        album_response['items'] += response['items']
        album_response['next'] = response['next']
    
    pick_data = pick_artist_data_from_json(artist_response, album_response, track_response)
    
    return pick_data


# ------------ Get Public Playlist Data by ID ---------------

def search_public_playlist_id(playlist_id):

    headers = create_header()
    
    playlist_response = requests.get(SPOTIFY_SEARCH_PUBLIC_PLAYLIST_ID_URL + playlist_id, headers=headers).json()
    
    params = {
        'limit': 50,
    }
    
    tracks_response = requests.get(SPOTIFY_SEARCH_PUBLIC_PLAYLIST_ID_URL + playlist_id + '/tracks', params=params, headers=headers).json()
    
    while tracks_response['next'] != None:
        
        params = {
            'limit': 50,
            'offset': len(tracks_response['items']),
        }
        
        response = requests.get(SPOTIFY_SEARCH_PUBLIC_PLAYLIST_ID_URL + playlist_id + '/tracks', params=params, headers=headers).json()
        
        tracks_response['items'] += response['items']
        tracks_response['next'] = response['next']
    
    pick_data = pick_playlist_data_from_json(playlist_response, tracks_response)
    
    return pick_data
