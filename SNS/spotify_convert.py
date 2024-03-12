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
                'image': item['album']['images'][0]['url'],
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
                'image': item['track']['album']['images'][0]['url'],
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
            'image': album_data['images'][0]['url'],
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
            'image': item['images'][0]['url'],
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
            'image': item['album']['images'][0]['url'],
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
        },
        'albums': response_album_data,
        'songs': response_song_data,
    }
    
    if 'images' in artist_res_data and len(artist_res_data['images']) > 0:
        response_data['artist']['image'] = artist_res_data['images'][0]['url']
    
    else:
        response_data['artist']['image'] = DEFAULT_ARTIST_IMAGE
    
    return response_data


# ------------ Pick Playlist Data from JSON ---------------

def pick_playlist_data_from_json(playlist_response, tracks_response):
    
    response_data = {}
    response_song_data = []
    
    for item in tracks_response['items']:
        
        if item['track'] != None:
            
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
                'image': item['track']['album']['images'][0]['url'],
            }
            
            track = {
                'song': song_data,
                'artist': artist_list,
                'album': album_data,
            }
            
            response_song_data.append(track)
    
    data_length = len(response_song_data)
    
    if 'offset' in tracks_response:
        offset = tracks_response['offset']
    else:
        offset = 0
    
    response_data = { 
        'status': {
            'success': data_length != 0,
            'one': data_length == 1,
            'total': data_length,
            'offset': offset,
        },
        'playlist': {
            'id': playlist_response['id'],
            'name': playlist_response['name'],
            'image': playlist_response['images'][0]['url'],
        },
        'songs': response_song_data,
    }
    
    return response_data


# ------------ Pick Any Data from JSON ---------------

def pick_any_data_from_json(search_response):
    
    response_data = {}
    response_song_data = {}
    
    for data_type in SPOTIFY_SEARCH_TYPE:
    
        response_song_data[data_type] = []
        
        for item in search_response[data_type]['items']:
            
            if data_type != 'playlists' and data_type != 'artists':
                
                artist_list = []
                
                for artist in item['artists']:
                    
                    artist_data = {
                        'id': artist['id'],
                        'name': artist['name'],
                    }
                    
                    if data_type == 'artists':
                        
                        artist_data['image'] = artist['images'][0]['url']
                    
                    artist_list.append(artist_data)
            
            elif data_type == 'artists':
                
                artist_data = {
                    'id': item['id'],
                    'name': item['name'],
                }
                
                if 'images' in item and len(item['images']) > 0:
                    artist_data['image'] = item['images'][0]['url']

                else:
                    artist_data['image'] = DEFAULT_ARTIST_IMAGE
            
            if data_type == 'artists':
                
                pick_data = {
                    'artist': artist_data,
                }
            
            elif data_type == 'albums':
                
                album_data = {
                    'id': item['id'],
                    'name': item['name'],
                    'image': item['images'][0]['url'],
                }
                
                pick_data = {
                    'artist': artist_list,
                    'album': album_data,
                }
            
            elif data_type == 'tracks':
                
                album_data = {
                    'id': item['album']['id'],
                    'name': item['album']['name'],
                    'image': item['album']['images'][0]['url'],
                }
                
                track_data = {
                    'id': item['id'],
                    'name': item['name'],
                    'preview': item['preview_url'],
                }
                
                pick_data = {
                    'artist': artist_list,
                    'album': album_data,
                    'track': track_data,
                }
            
            elif data_type == 'playlists':
                
                playlist_data = {
                    'id': item['id'],
                    'name': item['name'],
                    'image': item['images'][0]['url'],
                }
                
                pick_data = {
                    'playlist': playlist_data,
                }
            
            response_song_data[data_type].append(pick_data)
    
    data_length = max([len(response_song_data[data_type]) for data_type in SPOTIFY_SEARCH_TYPE])
    
    response_data = { 
        'status': {
            'success': data_length != 0,
            'one': data_length == 1,
            'total': data_length,
        },
        'data': response_song_data,
    }
    
    return response_data


# ------------ Pick Current Play Data from JSON ---------------

def pick_current_play_data_from_json(response):
    
    response_data = {
        'premium_user': True,
        
    } 
    
    return response_data
