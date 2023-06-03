import keyboard
import spotipy
import spotipy.util as util

# Spotify API credentials
SPOTIFY_USERNAME = 'your-username' # Add your username here
SPOTIFY_CLIENT_ID = 'your-id' # Add the client id you get here
SPOTIFY_CLIENT_SECRET = 'your-secret' # Add the client secret here
SPOTIFY_REDIRECT_URI = 'http://localhost:8080/'

# Spotify scope
SPOTIFY_SCOPE = 'user-modify-playback-state user-read-playback-state'

# Spotify access token
token = util.prompt_for_user_token(
    SPOTIFY_USERNAME,
    SPOTIFY_SCOPE,
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI
)

# Create a Spotify object
spotify = spotipy.Spotify(auth=token)

# Function to change the volume
def change_volume(volume_change):
    current_volume = spotify.current_playback()['device']['volume_percent']
    new_volume = max(0, min(100, current_volume + volume_change))
    spotify.volume(new_volume)

# Black magic I think
keyboard.add_hotkey('page up', lambda: change_volume(5), suppress=True) # Where Page Up is specified as Spotify volume up (find the list of valid key names here: https://github.com/boppreh/keyboard/blob/e277e3f2baf53ee1d7901cbb562f443f8f861b90/keyboard/_canonical_names.py)
keyboard.add_hotkey('page down', lambda: change_volume(-5), suppress=True) # Where Page Down is specified as Spotify volume down