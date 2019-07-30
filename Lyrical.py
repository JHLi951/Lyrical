import spotipy
import spotipy.util as util
import credentials
import pprint
# from PyLyrics import *
import lyricsgenius


def authenticate():
    token = util.prompt_for_user_token(
                                        credentials.USERNAME,
                                        credentials.SCOPE,
                                        client_id=credentials.CLIENT_ID,
                                        client_secret=credentials.CLIENT_SECRET,
                                        redirect_uri=credentials.REDIRECT_URI
    )


    return token

def get_song(sp):
    name = input("Enter an artist name: ")
    results = sp.search(q='artist:' + name, type='artist')
    pprint.pprint(results['artists']['items'][0])

def main():
    token = authenticate()

    if token:
        sp = spotipy.Spotify(auth=token)
        current_song = sp.currently_playing()

        current_song_artists = []
        for artist in current_song['item']['artists']:
            current_song_artists.append(artist['name'])

        current_song_name = current_song['item']['name']
        current_song_album = current_song['item']['album']['name']

        print(current_song_artists)
        print(current_song_name)
        print(current_song_album)

        genius = lyricsgenius.Genius(credentials.GENIUS_ACCESS_TOKEN)
        song_lyrics = genius.search_song(current_song_name, current_song_artists[0]).lyrics
        print(song_lyrics)
main()