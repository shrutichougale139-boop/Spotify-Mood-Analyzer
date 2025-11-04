import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-library-read"
))

results = sp.current_user_saved_tracks(limit=50)

song_names = []
energies = []
danceability = []
valence = []

for item in results['items']:
    track = item['track']
    song_names.append(track['name'])
    try:
        features = sp.audio_features(track['id'])[0]
        if features:
            energies.append(features['energy'])
            danceability.append(features['danceability'])
            valence.append(features['valence'])
        else:
            energies.append(None)
            danceability.append(None)
            valence.append(None)
    except:
        energies.append(None)
        danceability.append(None)
        valence.append(None)

df = pd.DataFrame({
    'Song': song_names,
    'Energy': energies,
    'Danceability': danceability,
    'Valence': valence
})

print(df.head())

plt.figure(figsize=(7,5))
df[['Energy', 'Danceability', 'Valence']].mean().plot(kind='bar', color=['#ff6f61', '#6fa8dc', '#93c47d'])
plt.title("🎧 Your Spotify Mood Profile")
plt.ylabel("Average Score")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
