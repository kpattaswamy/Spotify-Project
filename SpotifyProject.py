import spotipy 
import pandas as pd 
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

cid = " "
secret = ""
playlist_id = " "

creator = "kartik"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) #Converts ID into readable data
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #Gives us permission to access our spotify data
sp.trace = False
playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
#The above playlist stores all of the keys that we need to reference to extract and sort all of our data

def playlistData(creator, playlist_id):
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"] #gets track data from your playlist
    playlist_df = pd.DataFrame(columns = playlist_features_list) #Initializes dataframe with the columns from the above list
    
    for track in playlist: 
        playlist_features = {} 
        
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        audio_features = sp.audio_features(playlist_features["track_id"])[0] 
        
        for feature in playlist_features_list[4:]: 
            playlist_features[feature] = audio_features[feature]
        
        track_df = pd.DataFrame(playlist_features, index = [0]) 
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True) 
        
    return playlist_df

playlist_df = playlistData(creator, playlist_id) 
playlist_df.to_csv("SpotifyData.csv", index = False) 
        
    
playlist_df = playlistData(creator, playlist_id)
playlist_df.to_csv("SpotifyData.csv", index = False) 


column = playlist_df["energy"]
max_value = column.max() 
max_index = column.idxmax() 

print("Highest Energy Value:", max_value)
print("Most energetic song:", playlist_df["track"][max_index])
print("Top 15 Most Energetic Songs:")

largest = playlist_df.nlargest(15, 'energy')["track"] 

for x in largest:
    print(x)

min_value = column.min()
min_index = column.idxmin()

print("Least Energetic Value:", min_value)
print("Least energetic song:", playlist_df["track"][min_index])
print("Top 15 Least Energetic Songs:")

smallest = playlist_df.nsmallest(15, 'energy')["track"]

for x in smallest:
    print(x)
    
    
    

