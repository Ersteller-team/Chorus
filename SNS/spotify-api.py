#------------ Import Libraries ------------
import requests
import json
from .spotify_secret import *

# Set your Spotify API credentials
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET

#------------ Get Access Token ---------------
# Define the endpoint for obtaining an access token
token_url = 'https://accounts.spotify.com/api/token'

# Define the data to be sent in the request
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}

# Request the access token
response = requests.post(token_url, data=data)
print(response)

# Parse the JSON response
token_info = response.json()
print(token_info)

# Obtain the access token
access_token = token_info['access_token']

# Set the Authorization header with the access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept-Language': 'ja',
}

#------------ Search for Track ---------------
# Define the artist and track names
artist_name = 'Tele'
track_name = "ホムンクルス"

# Define the endpoint URL for track search
search_url = 'https://api.spotify.com/v1/search'

# Define the query parameters for track search
search_params = {
    'q': f'artist:{artist_name} track:{track_name}',
    'type': 'track',
    'limit': 30,
}

search_response = requests.get(search_url, headers=headers).json()

#------------ Search for Track by ID ---------------
track_id = '7KYZQay4ok85FWx1e5SweU'
search_url = 'https://api.spotify.com/v1/tracks/' + track_id
print(search_url)

# Make the API request for track saerch
search_response = requests.get(search_url, params=search_params,headers=headers).json()

# Output for response.json
with open('response.json', 'w', encoding='utf-8') as json_file:
    json.dump(search_response, json_file, ensure_ascii=False, indent=4)
    