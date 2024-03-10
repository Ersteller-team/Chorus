HOST_URL = 'http://localhost:8000'


# Spotify API Constants

SPOTIFY_AUTHENTICATE_SCOPE = 'user-read-playback-state user-read-currently-playing streaming playlist-read-private user-top-read user-read-recently-played user-library-read'


# Search types for Spotify API

SPOTIFY_SEARCH_TYPE_TRACK = 'track'

SPOTIFY_SEARCH_TYPE_ALBUM = 'album'

SPOTIFY_SEARCH_TYPE_ARTIST = 'artist'

SPOTIFY_SEARCH_TYPE_PLAYLIST = 'playlist'

SPOTIFY_REDIRECT_URI = HOST_URL + '/spotify/callback'

SPOTIFY_AUTHENTICATION_URL = 'https://accounts.spotify.com/authorize'

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1/'

SPOTIFY_SEARCH_TEXT_URL = SPOTIFY_API_BASE_URL + 'search/'

SPOTIFY_SEARCH_TRACK_ID_URL = SPOTIFY_API_BASE_URL + 'tracks/'

SPOTIFY_SAVED_TRACKS_URL = SPOTIFY_API_BASE_URL + 'me/tracks'

SPOTIFY_RECENT_PLAY_URL = SPOTIFY_API_BASE_URL + 'me/player/recently-played'



# Response Type

SPOTIFY_SEARCH_FOR_ITEM = 'search_for_item'

SPOTIFY_GET_TRACK = 'get_track'

SPOTIFY_SAVED_TRACKS = 'saved_tracks'

SPOTIFY_RECENT_PLAY = 'recent_play'

