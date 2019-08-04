import spotipy
import spotipy.util as util
import credentials
import pprint
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials


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
            song_lyrics = genius.search_song(current_song_name, current_song_artists[0]).lyrics
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
    playlists = sp.user_playlists('jellyli951')
    pprint.pprint(playlists)

# get_user_follow_info()
get_current_info()
