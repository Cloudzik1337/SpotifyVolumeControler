# SpotifyVolumeController (v2)

A lightweight script to control your Spotify desktop volume with hotkeys (default Page Up/Page Down), using a modern OAuth flow and environment-based configuration.

---
### Changelog:
- v2.0.0: Changed to use OAuth2 for authentication, added environment variable support, and improved error handling, added close from tray functionality also notifcation on windows system tray.
- v1.0.0: Initial release with basic functionality.

## 1. Create a Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in.  
2. Click **“Create an App”**, give it a name like “VolumeController”, and accept the terms.  
3. Copy your **Client ID** and **Client Secret** from the app’s **Dashboard**.  
4. Click **“Edit Settings”**, then under **Redirect URIs** add:  http://localhost:8080
5. Save.

## 2. Clone or Download This Repo

Place the files (`volume.py`, or `volume.pyw` if you prefer no console window) in a folder of your choice.

## 3. Create a `.env` File

In the same folder, create a file named `.env` with these contents:

```dotenv
#.env
SPOTIFY_USERNAME=your_spotify_username
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8080
```
## 5. Run the Script
With console output:

```py
python volume.py
```

You’ll see prompts the first time to authorize the app (copy the URL, log in, then paste the redirect URL).

Without any console window:

Rename volume.py → volume.pyw

Run it by double-clicking (Windows will use pythonw.exe and hide the console).

Once running, the script blocks forever (no exit key), and listens for **Page Up / Page Down** to adjust your Spotify volume.
To stop it, you'll need to **kill the process via Task Manager** or by **closing the associated Python window** (if you kept one).

## 6. Autostart on Login
##### A. Using the Startup Folder
Press ⊞ Win+R, type shell:startup, Enter.

In the opened folder, right-click → New → Shortcut.

Point it at your script:

If using volume.pyw:


```arduino
"C:\Path\To\volume.pyw"
```
Or explicitly:

```arduino
"C:\Path\To\pythonw.exe" "C:\Path\To\volume.pyw"
```

Name it e.g. “Spotify Volume Controller”.

##### B. Using Task Scheduler
Open Task Scheduler, choose Create Task…

On Triggers, click New… → At log on.

On Actions, click New…, set Program/script to:

```arduino
C:\Path\To\pythonw.exe
```
and Add arguments to:

```arduino
"C:\Path\To\volume.pyw"
```
(Optional) Under General, select “Run whether user is logged on or not” to fully hide any window.

Save.

## 7. (Optional) Rebinding Keys
By default the script listens for **page up / page down.** To rebind:

Edit volume.py and change the two lines in main():

```py
# volume.py
keyboard.add_hotkey('your_key_here',   lambda: change_volume(sp, +VOLUME_STEP), suppress=True)
keyboard.add_hotkey('your_other_key',  lambda: change_volume(sp, -VOLUME_STEP), suppress=True)
```
See the full list of key names in the keyboard repo [canonical names](https://github.com/boppreh/keyboard/blob/master/keyboard/_canonical_names.py)

# You’re all set! 🎉
Now your Spotify desktop volume can be cranked up or down with a simple keystroke, running silently in the background.
You can close script from tray or task manager.
## 8. Troubleshooting
Change logging level in `volume.py` to DEBUG to see more output. in `debug.log` file.
open issues on GitHub if needed.

## Icon by [Good Ware](https://www.flaticon.com/free-icons/levels) from [Flaticon](https://www.flaticon.com/)