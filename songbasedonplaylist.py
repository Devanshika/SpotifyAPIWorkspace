#This program lets user select a playlist and recommends a song 
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import random

username= "31tu3cd3yx6s4b6gcdtpelerisui"
scope= 'user-read-private user-read-playback-state user-modify-playback-state'

#erase cache and prompt for user permission

try:
    token=util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token=util.prompt_for_user_token(username, scope)
	
#create spotify object
spotipyObject=spotipy.Spotify(auth=token)

#user data
user= spotipyObject.current_user()
displayName=user['display_name']
print("Hi " +displayName+" lets get your playlists")
playlists=spotipyObject.current_user_playlists(limit=50, offset=0)

#print(json.dumps(playlists, sort_keys=True, indent=4))
playlists=playlists['items']
userPlaylist=[]
count = 0

#displaying userPlaylist
for item in playlists:
    count = count + 1
    userPlaylist.append([item['name'],item['id']])
    print(count,item['name'])

#asking user to select playlist
selectedPlaylist=input("Select playlist by serial no.")
selectedPlaylistId= userPlaylist[int(selectedPlaylist)-1][1]
tracks=spotipyObject.playlist_items(selectedPlaylistId, limit= 100)
#print(json.dumps(tracks,indent=4))
tracks=tracks['items']
songList=[]
sl=[]
for i in tracks: 
    songList.append([i['track']['name'], i['track']['id']])
    sl.append(i['track']['id'])    
selectedSongs=[]
#print(songList)
print(len(sl))
for i in range(5):
    n = random.randint(0,len(sl)-1)
    selectedSongs.append(sl[n])
print(selectedSongs)
recommendationSongs= spotipyObject.recommendations(seed_tracks= selectedSongs, limit=10)
recommendationSongs=recommendationSongs['tracks']
for i in recommendationSongs:
    print(i['name'])

#print(json.dumps(VARIABLE, sort_keys=True, indent=4))
