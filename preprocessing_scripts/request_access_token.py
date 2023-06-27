# How to run this:
# Replace client secret and client ID with actual Spotify API client secret/ID
# Run `python3 request_access_token.py`
# Copy access token (Valid for 1h)

import requests

url = "https://accounts.spotify.com/api/token"
CLIENT_SECRET = "your_client_secret"
CLIENT_ID = "your_client_id"
headers = {

    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
    token_type = token_data["token_type"]
    expires_in = token_data["expires_in"]
    print(f"Access Token: {access_token}")
    print(f"Token Type: {token_type}")
    print(f"Expires In: {expires_in} seconds")
else:
    print(f"Request failed with status code {response.status_code}")
