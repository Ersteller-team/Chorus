HOST_URL = 'https://music.ersteller.teraddition.com'


# Spotify API Constants

SPOTIFY_AUTHENTICATE_SCOPE = 'user-read-playback-state user-read-currently-playing streaming playlist-read-private user-top-read user-read-recently-played user-library-read user-read-private user-follow-read'


# Search types for Spotify API

SPOTIFY_SEARCH_TYPE_TRACK = 'track'

SPOTIFY_SEARCH_TYPE_ALL = 'track,album,artist,playlist'

SPOTIFY_REDIRECT_URI = HOST_URL + '/spotify/callback'

SPOTIFY_AUTHENTICATION_URL = 'https://accounts.spotify.com/authorize'

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1/'

SPOTIFY_SEARCH_TEXT_URL = SPOTIFY_API_BASE_URL + 'search/'

SPOTIFY_SEARCH_TRACK_ID_URL = SPOTIFY_API_BASE_URL + 'tracks/'

SPOTIFY_SEARCH_ALBUM_ID_URL = SPOTIFY_API_BASE_URL + 'albums/'

SPOTIFY_SEARCH_ARTIST_ID_URL = SPOTIFY_API_BASE_URL + 'artists/'

SPOTIFY_SEARCH_PLAYLIST_ID_URL = SPOTIFY_API_BASE_URL + 'playlists/'

SPOTIFY_USER_PROFILE_URL = SPOTIFY_API_BASE_URL + 'me'

SPOTIFY_SAVED_TRACKS_URL = SPOTIFY_USER_PROFILE_URL + '/tracks'

SPOTIFY_SAVED_ALBUMS_URL = SPOTIFY_USER_PROFILE_URL + '/albums'

SPOTIFY_FOLLOW_ARTISTS_URL = SPOTIFY_USER_PROFILE_URL + '/following'

SPOTIFY_GET_PLAYLISTS_URL = SPOTIFY_API_BASE_URL + 'users/'

SPOTIFY_CURRENT_PLAY_URL = SPOTIFY_USER_PROFILE_URL + '/player'

SPOTIFY_RECENT_PLAY_URL = SPOTIFY_CURRENT_PLAY_URL + '/recently-played'

SPOTIFY_CONTROL_START_URL = SPOTIFY_CURRENT_PLAY_URL + '/play'

SPOTIFY_CONTROL_PAUSE_URL = SPOTIFY_CURRENT_PLAY_URL + '/pause'

SPOTIFY_CONTROL_NEXT_URL = SPOTIFY_CURRENT_PLAY_URL + '/next'

SPOTIFY_CONTROL_PREVIOUS_URL = SPOTIFY_CURRENT_PLAY_URL + '/previous'

SPOTIFY_CONTROL_REPEAT_URL = SPOTIFY_CURRENT_PLAY_URL + '/repeat'

SPOTIFY_CONTROL_SHUFFLE_URL = SPOTIFY_CURRENT_PLAY_URL + '/shuffle'

SPOTIFY_SEARCH_TYPE = ['albums', 'artists', 'playlists', 'tracks']

DEFAULT_ARTIST_IMAGE = 'https://music-sns.s3.ap-northeast-1.amazonaws.com/default-artist.png'

DEFAULT_PLAYLIST_IMAGE = 'https://music-sns.s3.ap-northeast-1.amazonaws.com/default-playlist.png'



# Response Type

SPOTIFY_SEARCH_FOR_ITEM = 'search_for_item'

SPOTIFY_GET_TRACK = 'get_track'

SPOTIFY_SAVED_TRACKS = 'saved_tracks'

SPOTIFY_RECENT_PLAY = 'recent_play'

