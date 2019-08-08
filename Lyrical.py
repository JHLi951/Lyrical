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
                print("{}) Name: {},\
                        \n    Artists: {},\
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
                    print("Selected song number ", to_continue)
                    pprint.pprint(result['tracks']['items'][int(to_continue) - 1]['name'])
                    need_valid_input = False
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
