# **SpotifyVolumeControler**
KEEP IN MIND IT IS VERY EARLY PROJECT AND IT IS NOT FINISHED
Spotify Volume Controler allows you to control only spotify volume using wheel on keyboard
Spotify Volume Controler uses  [Spotipy](https://github.com/spotipy-dev/spotipy "Spotipy") to connect to spotify and control volume over web

## Setup
Create Spotify App
1. Go to [Spotify Developer](https://developer.spotify.com/dashboard/ "Spotify Developer") and login
2. Create App![CreateApp](https://cdn.upload.systems/uploads/s38kIZMc.png "Create App")
3. This Should Looks like this.                                                     
![](https://cdn.upload.systems/uploads/yMr2p6jY.png)
4. There is our **Client Id and Client Secret which we will use later**![](https://cdn.upload.systems/uploads/E3L1C3L7.png)

5. Download [VolumeControler.exe](https://github.com/Cloudzik1337/SpotifyVolumeControler/releases/download/1.0.1/VolumeControler.exe) or VolumeControler.py
6. Note: If u downloaded exe skip this step Run `py -m pip install Spotipy` and `py -m pip install pynput` in cmd
7. Then run VolumeControler You will be asked for for **Client Id**
8. Copy **Client Id**, **Client Secret**
9. Setup Deafult Volume (def vol is volume spotify will automaticly set after opening program)
10. Setup increasement (increasement is how much u will add to actual volume for ex. if increasement is 4 an volume is 50 after clicking f8 volume will change to 54)
11. Then you will be redictered to browser with spotify login
12. After Logging in you will be redictered to localhost http://localhost/?code....... which u have to copy and paste to VolumeControl.py
![](https://cdn.upload.systems/uploads/kIqzdS20.png)
13. If u have Done everything correctly you will see ![](https://cdn.upload.systems/uploads/k5ZYNs9z.png)
14. Use **F6** - Mute **F7** - Vol Down **F8** - Vol Up
15. And you are ready to go :D
