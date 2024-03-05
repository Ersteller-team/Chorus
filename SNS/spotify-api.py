#------------ Import Libraries ------------
import requests
import json

# Set your Spotify API credentials
client_id = "61bebe8bbccb4fc98273891e63515d08"
client_secret = "0faa7e3297264bd98e1dd2f8c8cd48b7"

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

# Parse the JSON response
token_info = response.json()

# Obtain the access token
access_token = token_info['access_token']

#------------ Search for Track ---------------
# Define the artist and track names
artist_name = 'Kenshi Yonezu'
track_name = "Lemon"

# Define the endpoint URL for track search
search_url = 'https://api.spotify.com/v1/search'

# Define the query parameters for track search
search_params = {
    'q': f'artist:{artist_name} track:{track_name}',
    'type': 'track',
    'limit': 30,
}

# Set the Authorization header with the access token
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Make the API request for track saerch
search_response = requests.get(search_url, params=search_params,headers=headers).json()

with open('response.json', 'w', encoding='utf-8') as json_file:
    json.dump(search_response, json_file, ensure_ascii=False, indent=4)

# Check for successful response for the track search
if search_response.status_code == 200:
    search_data = search_response.json()
    # Extract the track ID from the search results
    if 'tracks' in search_data and 'items' in search_data['tracks'] and search_data['tracks']['items']:
        track_id = search_data['tracks']['items'][0]['id']
        print(search_data)
        #--------------- Retrieve Audio Features --------------
        # Define endpoint URL for audio features
        audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'

        # Make the API request for audio features
        audio_features_response = requests.get(audio_features_url, headers=headers)

        # Check for successful response for audio features
        if audio_features_response.status_code == 200:
            audio_features_data = audio_features_response.json()
            # print(audio_features_data)

            # Save the audio features data to JSON file or do further processing
            with open('audio_features.json', 'w', encoding='utf-8') as json_file:
                json.dump(audio_features_data, json_file, ensure_ascii=False, indent=4)
        else:
            print(f"Error fetching audio features: {audio_features_response.status_code}")
    else:
        print(f"No track found for '{track_name}' by '{artist_name}'")
else:
    print(f"Error fetching track: {search_response.status_code}")