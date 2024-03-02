import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="518f553c577f40808b9bf5ccc5246a3d",
                                               client_secret="9fe45209294241eb97a8385cc0f35fd2",
                                               redirect_uri="http://127.0.0.1:8000/",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])