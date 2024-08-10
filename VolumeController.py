import time
import threading
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

VOLUME_UP_AMOUNT = 5
VOLUME_UP_KEY = 'page up'
VOLUME_DOWN_AMOUNT = -5
VOLUME_DOWN_KEY = 'page down'

volume_up_pressed = False
volume_down_pressed = False

# Spotify API credentials
SPOTIFY_USERNAME = 'your-username' # Add your username here
SPOTIFY_CLIENT_ID = 'your-id' # Add the client id you get here
SPOTIFY_CLIENT_SECRET = 'your-secret' # Add the client secret here
SPOTIFY_REDIRECT_URI = 'http://localhost:8080'

# Spotify scope
SPOTIFY_SCOPE = 'user-modify-playback-state user-read-playback-state'

# Global Spotify object
spotify = None

def refresh_token_periodically():
    global spotify
    while True:
        try:
            spotify.auth_manager.refresh_access_token(spotify.auth_manager.cache_handler.get_cached_token()['refresh_token'])
            logging.info("Token refreshed successfully.")
        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
        time.sleep(1800)  # Refresh every 30 minutes

def get_spotify_object():
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        username=SPOTIFY_USERNAME
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def change_volume(volume_change):
    global spotify
    try:
        logging.info(f"Hotkey pressed, attempting to change volume by {volume_change}.")
        playback = spotify.current_playback()
        if playback is None:
            logging.warning("No playback found, cannot change volume.")
            return
        current_volume = playback['device']['volume_percent']
        new_volume = max(0, min(100, current_volume + volume_change))
        spotify.volume(new_volume)
        logging.info(f"Volume changed to {new_volume}.")
    except spotipy.SpotifyException as e:
        logging.error(f"Spotify API error: {e}")
        # Recreate Spotify object in case of token expiration
        spotify = get_spotify_object()

def on_key_event(event):
    """Handle key press events."""
    if event.event_type == 'down':  # Trigger only on key down
        if event.name == VOLUME_UP_KEY and not volume_up_pressed:  # Volume up
            change_volume(VOLUME_UP_AMOUNT)
            volume_up_pressed = True
        elif event.name == VOLUME_DOWN_KEY and not volume_down_pressed:  # Volume down
            change_volume(VOLUME_DOWN_AMOUNT)
            volume_down_pressed = True
    elif event.event_type == 'up':
        if event.name == VOLUME_UP_KEY:
            volume_up_pressed = False
        elif event.name == VOLUME_DOWN_KEY: 
            volume_down_pressed = False

if __name__ == "__main__":
    try:
        # Create Spotify object
        spotify = get_spotify_object()

        # Start the token refresh thread
        token_refresh_thread = threading.Thread(target=refresh_token_periodically)
        token_refresh_thread.daemon = True  # Allows the thread to exit when the main program exits
        token_refresh_thread.start()

        # Set up hotkeys
        keyboard.hook(on_key_event)

        logging.info("Hotkeys registered, script is now running...")

        # Keep the script running to listen for hotkeys
        keyboard.wait()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
