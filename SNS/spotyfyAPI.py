import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

sp_oauth=SpotifyOAuth (
    client_id="518f553c577f40808b9bf5ccc5246a3d",
    client_secret="9fe45209294241eb97a8385cc0f35fd2",
    redirect_uri="http://127.0.0.1:8000/",
    scope="user-library-read",
    cache_path=".cache"
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='2d712b5d754849b7ab33bfbcf8ddd56d',
                                               client_secret='8ad7eda1216541b08e86577f15f9014f',
                                               redirect_uri='https://3c4f-240a-61-2c04-b974-8de6-86f6-51e7-766d.ngrok-free.app',
                                               scope='user-library-read',
                                               cache_path=".cache"))

auth_url = sp_oauth.get_authorize_url()
print(auth_url)
response = input("Enter the URL you were redirected to: ")

code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)



with open('.cache', 'r') as cache_file:
    cache_data = json.load(cache_file)

refresh_token = cache_data['refresh_token']
token_info = sp_oauth.refresh_access_token(refresh_token)
access_token = token_info['access_token']

sp = spotipy.Spotify(auth=access_token)





# Now you can use `sp` to call Spotify API

results = sp.current_user_saved_tracks()
for idx in results['items']:
    print(idx)


# Now you can use `sp` to call Spotify API
results = sp.current_user_saved_tracks()
for idx in results['items']:
    print(idx)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# クライアント情報とスコープを指定してSpotifyOAuthを初期化
sp_oauth = SpotifyOAuth(client_id="Y518f553c577f40808b9bf5ccc5246a3d",
                        client_secret="9fe45209294241eb97a8385cc0f35fd2",
                        redirect_uri="http://127.0.0.1:8000/",
                        scope="user-library-read")

# ブラウザで認証を行う
auth_url = sp_oauth.get_authorize_url()
print(auth_url)
response = input("Enter the URL you were redirected to: ")

# コールバックURLからアクセストークンを取得
code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)

# 新しいアクセストークンを取得
access_token = token_info['access_token']

# Spotipyクライアントを初期化
sp = spotipy.Spotify(auth=access_token)

# Spotify APIを使用して何かを行う
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])