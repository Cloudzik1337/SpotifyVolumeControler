import sys

import spotipy, threading, time
import os, json
import  logging

LOG_LEVEL = logging.CRITICAL # TOUCH ONLY IF YOUR PROGRAM CRASHES
LOG_TXT = 'log.txt'
# Define a function to handle the logging

logging.basicConfig(filename=LOG_TXT, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
# Set the window title
os.system('title SpotifyVolumeControler')

# Check if the settings file exists, if not create it and ask for the required information
path = os.getenv('APPDATA')
if not os.path.exists(path+'\\spotifyvolumecontrol.app'):
    # Create a dictionary with the required settings
    logging.debug('Settings file not found, creating one')
    jsonready ={
        "settings":{
            "client_id": input("[?] Client id : "),
            "client_secret": input("[?] Client Secret : "),
            "def_vol": input("[?] Default volume (def. 100) : "),
            "def_increasement": input("[?] Default increasement (def. 4) : ")
        }
    }
    # Write the dictionary to the file
    with open(path+'\\spotifyvolumecontrol.app', 'a+') as file:
        file.write(str(jsonready).replace("'", '"'))
        logging.debug('Settings file created')

# Read the settings from the file
with open(path+'\\spotifyvolumecontrol.app', 'r') as file:
    data = json.loads(file.read())
    logging.debug('Settings file read')

# Import the pynput library
from pynput import keyboard

# Assign the settings to variables
def_vol = int(data['settings']['def_vol'])

def_ammount = int(data['settings']['def_increasement'])
client_id = data['settings']['client_id']
client_secret = data['settings']['client_secret']

# Set the scope for the Spotify API
scope = 'user-read-currently-playing app-remote-control user-library-read user-read-playback-state streaming' 

# Wait until a device with Spotify is detected
for i in range(30):
    log = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id,client_secret, redirect_uri='http://localhost:8080/', scope=scope))
    logging.debug('Spotify API initialized')
    if log.current_playback() is None:
        time.sleep(1)
        print('[i] Waiting For Spotify',end='\r')
        logging.debug('Waiting for Spotify')
    else:
        os.system('cls')
        print('[i] Succesyfully Connected To Spotify!')
        logging.debug('Succesfully connected to Spotify')
        break

# Set the volume to the default value
log.volume(def_vol)

# Initialize the current volume as the default volume
act = def_vol

# Get the current playback information
log.current_playback()

# Define a function to print the current song and device information
def curr_soud(log):
    global act, def_vol, def_ammountm, prev_act
    i = 3
    old_track = ''
    while True:
        i += 1
        if i == 4:
            i = 0
            current = log.current_playback()
        try:
            # Get the device name, song name, and artist name
            device_name = current['device']['name']
            current_track = current['item']['name']
            curren_author = str(current['item']['album']['artists'][0]['name'])
            if old_track != current_track:
                os.system('cls')
                old_track = current_track
                logging.debug('Track changed')
                logging.debug('Current track: '+current_track)
                logging.debug('Current author: ' + curren_author)


            # Print the current song and device information
            if LOG_LEVEL is not logging.DEBUG:
                print(f'Currently Playing {current_track} by {curren_author} on device named {device_name} Volume: {act}                        ', end='\r')
            # Set the window title to the current song and device information
            os.system(f'title "SpotifyVolumeControler Currently Playing {current_track} by {curren_author} on device named {device_name} Volume: {act} "')

            time.sleep(0.15)
            
        except TypeError:

            logging.debug('No device found')
            # If there is no current song, print that and set the window title accordingly
            print(f'Currently Playing Nothin                        ', end='\r')
            os.system('title SpotifyVolumeControler Currently Playing Nothin ')

# Start the curr_soud function in a separate thread


curr_soudth = threading.Thread(target=curr_soud, args=[log])


curr_soudth.deamon = True
curr_soudth.start()
# Define a function to handle keyboard events
def on_press(key):
    try:
        global act, def_vol, def_ammountm, prev_act
        # Get the key pressed
        key = str(key).replace('Key.', '')
        if key == 'f7':
            # If the key is 'f7', decrease the volume by the default amount if it is above 0
            if act > -1:
                act = act- def_ammount
                log.volume(act)
                logging.debug('Decreased volume by '+str(def_ammount))
        elif key == 'f8':
            # If the key is 'f8', increase the volume by the default amount if it is below or equal to 100
            if act <= 100:
                act = act+ def_ammount
                log.volume(act)
                logging.debug('Increased volume by '+str(def_ammount))
        elif key == 'f6':
            # If the key is 'f6', mute the volume if it is not already muted, and unmute it if it is
            if act != 0:
                prev_act = act
                act = 0
                log.volume(act)
            else:
                log.volume(prev_act)
                act = prev_act
            logging.debug('Muted/Unmuted volume')
    except:
        pass

# Start the keyboard listener
listenerth = keyboard.Listener(on_press=on_press)
listenerth.daemon = True
listenerth.start()
listenerth.join()

logging.debug('Program ended all threads closed')
sys.exit()
