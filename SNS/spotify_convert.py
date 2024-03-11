# ------------ Import Libraries ------------
from .constants import *


# ------------ Pick Song Data from JSON ---------------

def pick_song_data_from_json(data, type):
    
    response_data = {}
    response_song_data = []
    
    if type == SPOTIFY_SEARCH_FOR_ITEM:
        pick_data = data['tracks']['items']
    elif type == SPOTIFY_GET_TRACK:
        pick_data = [data]
    elif type == SPOTIFY_SAVED_TRACKS or type == SPOTIFY_RECENT_PLAY:
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
    
    elif type == SPOTIFY_SAVED_TRACKS or type == SPOTIFY_RECENT_PLAY:
        
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
    
    if 'offset' in data:
        offset = data['offset']
    else:
        offset = 0
    
    response_data = { 
        'status': {
            'success': data_length != 0,
            'one': data_length == 1,
            'total': data_length,
            'offset': offset,
        },
        'data': response_song_data,
    }
    
    return response_data


# ------------ Pick Album Data from JSON ---------------

def pick_album_data_from_json(album_data, track_data):
    
    response_data = {}
    response_song_data = []
        
    for item in track_data['items']:
        
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
        
        track = {
            'song': song_data,
            'artist': artist_list,
        }
        
        response_song_data.append(track)
    
    data_length = len(response_song_data)
    
    offset = 0
    
    artist_list = []
    
    for artist in album_data['artists']:
        
        artist_data = {
            'id': artist['id'],
            'name': artist['name'],
        }
        
        artist_list.append(artist_data)
    
    response_data = { 
        'status': {
            'success': data_length != 0,
            'one': data_length == 1,
            'total': data_length,
            'offset': offset,
        },
        'album': {
            'id': album_data['id'],
            'name': album_data['name'],
            'image': album_data['images'][1]['url'],
            'artist': artist_list,
        },
        'songs': response_song_data,
    }
    
    return response_data


# ------------ Pick Artist Data from JSON ---------------

def pick_artist_data_from_json(artist_res_data, album_data, track_data):
    
    response_data = {}
    response_album_data = []
    response_song_data = []
    
    for item in album_data['items']:
        
        album_data = {
            'id': item['id'],
            'name': item['name'],
            'image': item['images'][1]['url'],
        }
        
        artist_list = []
        
        for artist in item['artists']:
            
            artist_data = {
                'id': artist['id'],
                'name': artist['name'],
            }
            
            artist_list.append(artist_data)
        
        album = {
            'album': album_data,
            'artist': artist_list,
        }
        
        response_album_data.append(album)
    
    
    for item in track_data['tracks']:
        
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
    
    data_length = len(response_album_data)
    
    offset = 0
    
    artist_list = []
    
    response_data = { 
        'status': {
            'success': data_length != 0,
            'one': data_length == 1,
            'total': data_length,
            'offset': offset,
        },
        'artist': {
            'id': artist_res_data['id'],
            'name': artist_res_data['name'],
            'image': artist_res_data['images'][1]['url'],
        },
        'albums': response_album_data,
        'songs': response_song_data,
    }
    
    return response_data
