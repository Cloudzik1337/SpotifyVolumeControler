import spotipy, threading, time
import os, json







path = os.getenv('APPDATA')
if not os.path.exists(path+'\\spotifyvolumecontrol.app'):
    jsonready ={
"settings":{
    "client_id": input("[?] Client id : "),
    "client_secret": input("[?] Client Secret : "),
    "def_vol": input("[?] Deafult volume (def. 100) : "),
    "def_increasement": input("[?] Deafult increasement (def. 4) : ")
}}
    with open(path+'\\spotifyvolumecontrol.app', 'a+') as file:
        file.write(str(jsonready).replace("'", '"'))


with open(path+'\\spotifyvolumecontrol.app', 'r') as file:
    data = json.loads(file.read())
from pynput import keyboard
def_vol = int(data['settings']['def_vol'])
def_ammount = int(data['settings']['def_increasement'])
client_id = data['settings']['client_id']
client_secret = data['settings']['client_secret']
scope = 'user-read-currently-playing app-remote-control user-library-read user-read-playback-state streaming' 
for i in range(30):
    
        log = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id,client_secret, redirect_uri='http://localhost/', scope=scope))
        if log.current_playback() == None:
            time.sleep(1)
            print('[i] Waiting For Spotify',end='\r')
        else:
            os.system('cls')
            print('[i] Succesyfully Connected To Spotify!')
            break
            
       

  


log.volume(def_vol)
act = def_vol
log.current_playback()
def curr_soud(log):
    global act, def_vol, def_ammountm, prev_act
    while True:
        
        current = log.current_playback()
        
        try:
            device_name = current['device']['name']
            current_track = current['item']['name']
            curren_author = current['item']['album']['artists'][0]['name']
        except TypeError:
            print(f'Currently Playing Nothin                        ', end='\r')
        print(f'Currently Playing {current_track} by {curren_author} on device named {device_name} Volume: {act}                        ', end='\r')
        time.sleep(1)

threading.Thread(target=curr_soud, args=[log]).start()

def on_press(key):
    try:
        global act, def_vol, def_ammountm, prev_act
        key = str(key).replace('Key.', '')
        if key == 'f7':
            if act > -1:
                act = act- def_ammount
                log.volume(act)

        elif key == 'f8':
            if act <= 100:
                act = act+ def_ammount
                log.volume(act)

        elif key == 'f6':
            if act != 0:
                prev_act = act
                act = 0
                log.volume(act)
            else:
                log.volume(prev_act)
                act = prev_act
    except:
        pass
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
