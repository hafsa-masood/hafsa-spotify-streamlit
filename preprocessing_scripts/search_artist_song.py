import requests
import json

def get_song_details(song_name, artist_name, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": f"track:{song_name} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["tracks"]["items"]:
            track = data["tracks"]["items"][0]
            return True
        else:
            return False
    else:
        return False

def get_show_data(show_name, episode_name, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": f"show:{show_name} episode:{episode_name}",
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["tracks"]["items"]:
            track = data["tracks"]["items"][0]
            return True
        else:
            return False
    else:
        return False

def get_track_category(artist_name, track_name, access_token):
    if get_song_details(track_name, artist_name, access_token):
        return "song"
    elif get_show_data(artist_name, track_name, access_token):
        return "podcast"
    else:
        return "other"