import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#get username
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

#get current device 
devices=spotipyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceId=devices['devices'][0]['id']

#getting current track information
track=spotipyObject.current_user_playing_track()
print(json.dumps(track, sort_keys=True, indent=4))
print()
artist=track['item']['artists'][0]['name']
track=track['item']['name']
if artist !="":
    print("Currently playing" +artist+ " "+track)
   
#user data
user= spotipyObject.current_user()
displayName=user['display_name']
followers=user['followers']['total']
while True:
    print()
    print("welcome to SPOTIPY " +displayName+ "You have followers: " + str(followers))
    print(">>>>")
    print("1 for search an artist")
    print("0 for exit")
    choice=input("Enter your choice:")

#search artist    
    if choice=="1":
        searchQuery=input("Enter artist")
        print()

        #get search results
    
        searchResults=spotipyObject.search(searchQuery, 1,0,"artist")
        
        artist=searchResults['artists']['items'][0]
        print(artist['name'])
        print("Number of followers: "+ str(artist['followers']['total']))
        print(artist['genres'][0])
        artistID=artist['id']
        print()
        webbrowser.open(artist['images'][0]['url'])

#album and track details
        trackURIs=[]
        trackArt=[]
        z=0
    
#extract album data
        albumResults=spotipyObject.artist_albums(artistID)
        albumResults=albumResults['items']
        for item in albumResults:
            print("album" +item['name'])
            albumID=item['id']
            albumArt=item['images'][0]['url']
            
           #extract track data
            trackResults=spotipyObject.album_tracks(albumID)
            trackResults=trackResults['items']
            for item in trackResults:
                print(str(z)+ ":" + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z=z+1
            print()
           
           #see album art
            while True:
                songSelection=input("Enter song number to see art and play song or press x to exit")
                if songSelection == 'x':
                    break
                trackselectionList=[]
                trackselectionList.append(trackURIs[int(songSelection)])
                spotipyObject.start_playback(deviceId, None, trackselectionList)
                webbrowser.open(trackArt[int(songSelection)])
                
                
#end program
    if choice=="0":
        break
#print(json.dumps(VARIABLE, sort_keys=True, indent=4))
