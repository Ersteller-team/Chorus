# ------------ Import Libraries ------------
import requests
from .spotify_secret import *
from .spotify_url import *


# ------------ Get No Authentication Access Token ---------------

def get_access_token_no_authentication() -> dict[str, str]:
    
    data: dict[str, str] = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    
    token_response: dict = requests.post(SPOTIFY_TOKEN_URL, data=data).json()
    access_token: str = token_response['access_token']
    
    response: dict = {
        'Authorization': f'Bearer {access_token}',
        'Accept-Language': 'ja',
    }
    
    return response


# ------------ Pick Data from JSON ---------------

def pick_data_from_json(get_data: dict) -> dict[str, any]:
    
    response_data: dict[str, any] = {}
    response_song_data: list = []
    
    for item in get_data['tracks']['items']:
        
        song_data: dict = {
            'id': item['id'],
            'name': item['name'],
            'preview': item['preview_url'],
        }
        
        artist_list: list = []
        
        for artist in item['artists']:
            
            artist_data: dict = {
                'id': artist['id'],
                'name': artist['name'],
            }
            
            artist_list.append(artist_data)
        
        album_data: dict = {
            'id': item['album']['id'],
            'name': item['album']['name'],
            'image': item['album']['images'][1]['url'],
        }
        
        track: dict = {
            'song': song_data,
            'artist': artist_list,
            'album': album_data,
        }
        
        response_song_data.append(track)
    
    if response_song_data == []:
        response_data = { 'status': {'about': 'Failure', 'total': len(response_song_data)}, 'data': response_song_data }
    
    else:
        response_data = { 'status': {'about': 'Success', 'total': len(response_song_data)}, 'data': response_song_data }
    
    return response_data


# ------------ Search for Query ---------------

def search_query(type: list[str], query: str, limit: int = 20, offset: int = 0) -> dict[str, any]:

    headers: dict = get_access_token_no_authentication()
    
    search_params: dict = {
        'q': query,
        'type': type,
        'limit': limit,
        'offset': offset,
    }
    
    response: dict[str, any] = requests.get(SPOTIFY_SEARCH_TEXT_URL, params=search_params, headers=headers).json()
    
    pick_data: dict[str, any] = pick_data_from_json(response)
    
    return pick_data


# ------------ Search for Track & Artist ---------------

def search_track_artist(type: list[str], track: str | None = None, artist: str | None = None, limit: int = 20, offset: int = 0) -> dict[str, dict[str, str | int] | list[dict[str, str | int]]]:
    
    query: str = ""
    
    if artist != None:
        query = 'artist:' + artist + ' '
    
    if track != None:
        query += 'track:' + track
    
    return search_query(type, query, limit, offset)


# ------------ Search for Track by ID ---------------

def search_track_id(track_id: str) -> dict[str, any]:

    headers: dict = get_access_token_no_authentication()
    
    response: dict = requests.get(SPOTIFY_SEARCH_TRACK_ID_URL + track_id, headers=headers).json()
    
    pick_data: dict = pick_data_from_json(response)
    
    return pick_data
