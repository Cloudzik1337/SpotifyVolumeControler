#!/usr/bin/env pythonw
# -*- coding: utf-8 -*-
"""
Spotify Volume Control

This script allows you to adjust your Spotify playback volume using
global hotkeys (Page Up / Page Down) and provides system notifications
and a tray icon for feedback. It uses Spotipy for Spotify API access,
python-dotenv for configuration, win10toast for Windows toasts, and
pystray + PIL for a system tray icon.


07-05-2025
Author: github.com/cloudzik1337

This update includes:
- Added a tray icon with an 'Exit' menu item.
- Added a notification system using win10toast.
- Added a cooldown period to prevent rate-limiting by the Spotify API.
- Added a logging system with rotation for the debug log.
- Added a revive mechanism to restart the script on unexpected errors.

ChatGPT o4-mini-high helped me clear up the code 
"""

import logging
import os
import time
from threading import Event
from sys import platform
from webbrowser import open as open_browser

import keyboard
import spotipy
from dotenv import load_dotenv
from PIL import Image
from pystray import Icon, MenuItem, Menu
from spotipy.oauth2 import SpotifyOAuth
from win10toast import ToastNotifier

# ─── Configuration ────────────────────────────────────────────────────────────

# Spotify OAuth scope
SCOPE = "user-modify-playback-state user-read-playback-state"

# How much to change volume with each hotkey press (in percent)
VOLUME_STEP = 10

# Minimum time (in seconds) between successive volume changes
COOLDOWN = 0.2

# Maximum size (bytes) of debug log file before rotation
MAX_LOG_SIZE = 3 * 1024 * 1024  # 3 MB

# Logging level: DEBUG for development, INFO for normal use
LOG_LEVEL = logging.DEBUG

# Path to the tray icon image 
ICON_PATH = "program.png"


# ─── Logging Setup ────────────────────────────────────────────────────────────

LOG_FORMAT = (
    "%(asctime)s │ %(levelname)-8s │ %(name)-12s │ %(message)s"
)
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

if LOG_LEVEL == logging.INFO:
    # Rotate debug.log if it grows too large
    if os.path.exists("debug.log") and os.path.getsize("debug.log") > MAX_LOG_SIZE:
        os.remove("debug.log")

    file_handler = logging.FileHandler("debug.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)
    logger.debug("Debug logging enabled")


# ─── Tray & Notifications ─────────────────────────────────────────────────────

def on_exit(icon, item) -> None:
    """
    Handler for the 'Exit' menu item in the system tray.
    Stops the tray icon, clears hotkeys, logs, and exits the process cleanly.
    """
    logger.info("Exit requested via tray menu")
    icon.stop()
    keyboard.unhook_all_hotkeys()
    logger.info("Cleared all hotkeys")
    os._exit(0)


def setup_tray() -> None:
    """
    Initializes and displays a system tray icon with an 'Exit' menu item.
    Runs detached so the main thread is free to set up hotkeys/Spotify.
    """
    tray_menu = Menu(MenuItem("Exit", on_exit))
    tray_icon = Icon(
        name="SpotifyVol",
        icon=Image.open(ICON_PATH),
        title="Spotify Volume Control",
        menu=tray_menu,
    )
    tray_icon.run_detached()
    logger.info("Tray icon set up")


def notify(title: str, message: str) -> None:
    """
    Shows a system notification. Currently implemented for Windows using win10toast.
    """
    if platform == "win32":
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=2)
        logger.debug("Notification shown: %s – %s", title, message)


# ─── Spotify Authentication ───────────────────────────────────────────────────

def load_credentials() -> dict:
    """
    Loads Spotify credentials from environment variables.
    Expects SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI.
    Raises RuntimeError if any are missing.
    """
    load_dotenv()
    required_keys = [
        "SPOTIFY_USERNAME",
        "SPOTIFY_CLIENT_ID",
        "SPOTIFY_CLIENT_SECRET",
        "SPOTIFY_REDIRECT_URI",
    ]
    creds = {key: os.getenv(key) for key in required_keys}
    missing = [key for key, val in creds.items() if not val]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")
    logger.debug("Environment credentials loaded")
    return creds


def get_spotify_client(creds: dict) -> spotipy.Spotify:
    """
    Authenticates with Spotify via OAuth and returns a Spotipy client.
    Uses a cache file (.cache-<username>) for tokens and auto-refresh.
    """
    oauth = SpotifyOAuth(
        client_id=creds["SPOTIFY_CLIENT_ID"],
        client_secret=creds["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=creds["SPOTIFY_REDIRECT_URI"],
        scope=SCOPE,
        username=creds["SPOTIFY_USERNAME"],
        cache_path=f".cache-{creds['SPOTIFY_USERNAME']}",
    )

    token_info = oauth.get_cached_token()
    if not token_info:
        auth_url = oauth.get_authorize_url()
        open_browser(auth_url)
        logger.info("If browser does not open, please visit: %s", auth_url)
        response = input("Paste the full redirect URL here: ")
        if "code=" in response:
            response = response.split("code=")[1]
        token_info = oauth.get_access_token(response)

    logger.debug("Spotify OAuth authentication complete")
    return spotipy.Spotify(auth_manager=oauth)


# ─── Volume Control Logic ──────────────────────────────────────────────────────

def change_volume(sp_client: spotipy.Spotify, delta: int) -> None:
    """
    Adjusts the Spotify playback volume by 'delta' percent.
    Respects a cooldown period to avoid spamming the API.
    """
    current_time = time.time()
    if not hasattr(change_volume, "last_time"):
        change_volume.last_time = 0.0

    if current_time - change_volume.last_time < COOLDOWN:
        return

    change_volume.last_time = current_time
    playback = sp_client.current_playback()

    if not playback or not playback.get("device"):
        logger.warning("No active Spotify device found.")
        return

    current_vol = playback["device"]["volume_percent"]
    new_vol = max(0, min(100, current_vol + delta))

    if new_vol != current_vol:
        try:
            sp_client.volume(new_vol)
            logger.info("Volume set to %d%%", new_vol)
        except spotipy.SpotifyException as e:
            logger.error("Failed to set volume: %s", e)


# ─── Main Application ──────────────────────────────────────────────────────────

def main() -> None:
    """
    Entry point for the volume control logic.
    Loads credentials, authenticates, registers hotkeys, and waits indefinitely.
    """
    # Set console title on Windows
    if platform == "win32":
        os.system("title Spotify Volume Control")

    logger.info("Starting Spotify Volume Control")
    creds = load_credentials()
    sp_client = get_spotify_client(creds)

    # Register global hotkeys
    keyboard.add_hotkey("page up", lambda: change_volume(sp_client, +VOLUME_STEP), suppress=True)
    keyboard.add_hotkey("page down", lambda: change_volume(sp_client, -VOLUME_STEP), suppress=True)
    logger.info("Hotkeys registered: Page Up / Page Down")

    # Notify user and wait until interruption
    notify("Spotify Volume Control", "Service is now running")
    Event().wait()


if __name__ == "__main__":
    setup_tray()
    # Run in a loop to auto-restart on unexpected errors
    while True:
        try:
            main()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected, exiting...")
            os._exit(0)
        except Exception as e:
            logger.error("Unhandled exception: %s", e)
            notify("Spotify Volume Control", f"Error occurred: {e}")
            time.sleep(5)
            logger.info("Restarting Spotify Volume Control")
            notify("Spotify Volume Control", "Restarting...")
            continue
