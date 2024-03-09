# ------------ Import Libraries ------------
from .constants import *


# ------------ Pick Data from JSON ---------------

def pick_song_data_from_json(data, type):
    
    response_data = {}
    response_song_data = []
    
    if type == SPOTIFY_SEARCH_FOR_ITEM:
        pick_data = data['tracks']['items']
    elif type == SPOTIFY_GET_TRACK:
        pick_data = [data]
    elif type == SPOTIFY_SAVED_TRACKS:
        pick_data = data['items']
    
    if type == SPOTIFY_SEARCH_FOR_ITEM or type == SPOTIFY_GET_TRACK:
        
        for item in pick_data:
            
            song_data = {
                'id': item['id'],
                'name': item['name'],
                'preview': item['preview_url'],
            }
            
            artist_list = []
            
            for artist in item['artists']:
                
                artist_data = {
                    'id': artist['id'],
                    'name': artist['name'],
                }
                
                artist_list.append(artist_data)
            
            album_data = {
                'id': item['album']['id'],
                'name': item['album']['name'],
                'image': item['album']['images'][1]['url'],
            }
            
            track = {
                'song': song_data,
                'artist': artist_list,
                'album': album_data,
            }
            
            response_song_data.append(track)
    
    elif type == SPOTIFY_SAVED_TRACKS:
        
        for item in pick_data:
            
            song_data = {
                'id': item['track']['id'],
                'name': item['track']['name'],
                'preview': item['track']['preview_url'],
            }
            
            artist_list = []
            
            for artist in item['track']['artists']:
                
                artist_data = {
                    'id': artist['id'],
                    'name': artist['name'],
                }
                
                artist_list.append(artist_data)
            
            album_data = {
                'id': item['track']['album']['id'],
                'name': item['track']['album']['name'],
                'image': item['track']['album']['images'][1]['url'],
            }
            
            track = {
                'song': song_data,
                'artist': artist_list,
                'album': album_data,
            }
            
            response_song_data.append(track)
    
    data_length = len(response_song_data)
    
    if response_song_data == 0:
        response_data = { 'status': { 'success': False, 'total': 0, 'one': False }, 'data': response_song_data }
    
    else:
        response_data = { 'status': { 'success': True, 'total': data_length, 'one': data_length == 1 }, 'data': response_song_data }
    
    return response_data