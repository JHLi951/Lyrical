import spotipy
import spotipy.util as util
import credentials
import pprint
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np


def authenticate(scope):
    token = util.prompt_for_user_token(
                                        credentials.USERNAME,
                                        scope,
                                        client_id=credentials.CLIENT_ID,
                                        client_secret=credentials.CLIENT_SECRET,
                                        redirect_uri=credentials.REDIRECT_URI
    )

    return token


def get_current_info():
    lyrics = ""
    token = authenticate('user-read-currently-playing')

    # If the token is valid, gets the current playing song
    # and displays the artists, song name, song album, and song lyrics
    if token:
        sp = spotipy.Spotify(auth=token)
        current_song = sp.currently_playing()
        current_song_artists = []
        for artist in current_song['item']['artists']:
            current_song_artists.append(artist['name'])

        current_song_name = current_song['item']['name']
        current_song_album = current_song['item']['album']['name']

        # print("Artists:", current_song_artists)
        # print("Song Name:", current_song_name)
        # print("Song Album:", current_song_album)
        # print("~~~~~~~~~~~~~~~~~~~~~~~")

        genius = lyricsgenius.Genius(credentials.GENIUS_ACCESS_TOKEN)
        
        try:
            song_lyrics = genius.search_song(current_song_name, current_song_artists[0])
            song_lyrics = song_lyrics.lyrics
            # print(song_lyrics)
            lyrics = song_lyrics
        except:
            print("Song lyrics not found on Genius")

        return current_song_artists, current_song_name, current_song_album, lyrics
    else:
        print("Need a valid token")


def get_user_follow_info():
    token = authenticate('user-follow-read')

    if token:
        sp = spotipy.Spotify(auth=token)
        following = sp.current_user_followed_artists(limit=50)
        followed_artists = []
        for artist in following['artists']['items']:
            followed_artists.append(artist['name'])
        print(followed_artists)
    else:
        print("Need a valid token")


def make_acronym_playlist(acronym):
    token = authenticate('playlist-modify-public')

    if token:
        sp = spotipy.Spotify(auth=token)
        letters = [c for c in acronym]
        # for letter in letters:
        pprint.pprint(sp.search(q=letters[0], type='track'))

    else:
        print("Need a valid token")


def check_client_credentials_flow():
    #testing use of client credentials flow
    client_credentials_manager = SpotifyClientCredentials(
        client_id=credentials.CLIENT_ID,
        client_secret=credentials.CLIENT_SECRET
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists(credentials.USERNAME)
    pprint.pprint(playlists)


def search_song():
    token = authenticate('')

    if token:
        song_searched = input("Enter desired song: ")        
        sp = spotipy.Spotify(auth=token)

        counter = 1
        pagecounter = 0
        next_page = True
        page_size = 5

        while(next_page):
            result = sp.search( song_searched, 
                                limit=page_size, 
                                offset=pagecounter*page_size)

            print("Page number", pagecounter)
            print("~~~~~~~~~~~~~~~")

            for song in result['tracks']['items']:
                name = song['name']
                artists = []
                for artist in song['artists']:
                    artists.append(artist['name'])
                album = song['album']['name']
                print("{}) Name: {}\
                        \n    Artists: {}\
                        \n    Album: {}\n".format(counter, name, artists, album))
                counter += 1
            
            need_valid_input = True

            while need_valid_input:
                to_continue = input("Enter song number, \"next\" for next page of results, \"prev\" for previus page, or \"esc\" to quit: ")

                if to_continue == "next":
                    pagecounter += 1
                    need_valid_input = False
                elif to_continue == "prev":
                    counter -= page_size*2
                    pagecounter -= 1
                    need_valid_input = False
                elif string_is_int(to_continue):
                    next_page = False
                    need_valid_input = False
                    print("Selected song number", to_continue)
                    # pprint.pprint(result['tracks']['items'][int(to_continue) - 1]['name'])
                    return (result['tracks']['items'][int(to_continue) - 1]['name'], result['tracks']['items'][int(to_continue) - 1]['id'])
                    
                elif to_continue == "esc":
                    next_page = False
                    need_valid_input = False
                else:
                    print("Enter Valid Input")
                    need_valid_input = True

    else:
        print("Invalid token")


def string_is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_song_audio_analysis():
    token = authenticate('')

    if token:
        song_name, song_id = search_song()
        sp = spotipy.Spotify(auth=token)

        result = sp.audio_analysis(song_id)
        with open('{}_audio_analysis.txt'.format(song_name), 'w') as f:
            pprint.pprint(result, f)
        print("Text file created successfully")
    else:
        print("Invalid token")





# Given a playlist, returns an ordered list of the most danceable songs in the playlist
# Functions used: authenticate, get_playlists, get_danceability
def get_playlist_most_danceable_songs(playlist):
    token = authenticate('')

    if token:
        sp = spotipy.Spotify(auth=token)
        users_playlists = get_playlists(sp)
        playlist_songs = []

        if playlist in users_playlists:
            playlist_id = users_playlists[playlist]
        else:
            print("Invalid playlist")

        results = get_playlist_songs(playlist_id, sp)

        for song in results['items']:
            song_id = song['track']['id']
            song_name = song['track']['name']
            song_score = get_feature(song_id, 'danceability', sp)

            playlist_songs.append((song_name, song_score))

        playlist_songs.sort(key=lambda x: x[1], reverse=True)
        return playlist_songs

    else:
        print("Invalid token")


# Get all playlists for the current user and returns a dictionary with 
# playlist names mapped to their playlist IDs
def get_playlists(sp):
    playlists = {}

    results = sp.user_playlists(credentials.USERNAME)
        
    for playlist in results['items']:
        playlists[playlist['name']] = playlist['id']

    return playlists


def get_playlist_songs(playlist_id, sp):
    results = sp.user_playlist_tracks(
        credentials.USERNAME,
        playlist_id
    )

    return results

# Given a song (in the form of the song id), returns the audio features
def get_audio_features(song_id, sp):
    return sp.audio_features(song_id)

    
# Given a song id, extracts and returns the danceability from the audio features
# Functions used: get_audio_features
def get_feature(song_id, feature, sp):
    features = get_audio_features(song_id, sp)
    return features[0][feature]


# List of features: duration_ms, key, mode, time_signature,
#   acousticness, danceability, energy, instrumentalness,
#   liveness, loudness, speechiness, valence, tempo. id, uri
#   track_href, analysis_url, type
def graph_playlist_feature(playlist_name, feature):
    token = authenticate("")

    if token:
        sp = spotipy.Spotify(auth=token)

        X = []
        y = []

        playlists = get_playlists(sp)
        if playlist_name in playlists:
            playlist_id = playlists[playlist_name]

        playlist_songs = get_playlist_songs(playlist_id, sp)

        for song in playlist_songs['items']:  
            song_name = song['track']['name']
            X.append(song_name)
            song_id = song['track']['id']
            speech_level = get_feature(song_id, feature, sp)
            y.append(speech_level)

        index = np.arange(len(X))
        plt.bar(index, y)
        plt.xlabel('Song')
        plt.ylabel('Value')
        plt.xticks(index, X, rotation=90)
        plt.title("{} Values ({})".format(feature, playlist_name))
        plt.show()

    else:
        print("Invalid token")
    


# pprint.pprint(get_playlist_most_danceable_songs('calm'))
# graph_playlist_feature('Joe\'s World', 'tempo')