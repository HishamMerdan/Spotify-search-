import requests
import base64
import json

# Create a dashboard on Spotify and name it. In this dashboard, you will find the client ID and the client secret.
client_id = "" # change it to you own id  
client_secret = "" # change it to you own secret  

def get_token():
    """
    Function to get the authorization token from Spotify API.
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    """
    Function to get the authorization header using the token.
    """
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    """
    Function to search for an artist by name.
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"  # artist_name can be changed to album name or anything else depending on the required result.
    query_url = url + query
    result = requests.get(query_url, headers=headers)
    
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    """
    Function to get top tracks by artist ID.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=DE"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    print(result)

    if result.status_code != 200:
        print(f"Error: {result.status_code}")
        return []

    json_result = json.loads(result.content)["tracks"]
    return json_result

# Main script
token = get_token()

result = search_for_artist(token, "beastboy")  # Enter the artist you want to get data for
if result:
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)

    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}, Link: {song['href']}")

else:
    print("Artist not found.")
