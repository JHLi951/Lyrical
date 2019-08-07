import Lyrical
import uuid
import queue


class User:
    def __init__(self, name, password):
        self.user_name = name
        self.user_password = password
        self.user_id = uuid.uuid4()

    def change_password(self, current_password, new_password):
        if current_password == self.user_password:
            self.user_password = new_password



class Lobby:

    # Initializes basic lobby information and holds

    def __init__(self, name, password, owner):
        self.lobby_name = name
        self.lobby_password = password
        self.lobby_owner = owner
        self.lobby_id = uuid.uuid1()
        self.members = [owner]
        self.playlist_queue = queue.Queue(0)
        self.added_queue = queue.Queue(0)

    # def create_playlist_queue(self, owner, playlist_name):


    def change_password(self, user, new_password):
        if user.user_id == self.lobby_owner.user_id:
            self.lobby_password = new_password


    def add_member(self, user, entered_password):
        if entered_password == self.lobby_password:
            self.members.append(user)

    def add_song_to_queue(self, member, song_name):
        member_name = member.user_name

        self.added_queue.put((song_name, member_name))

    def play_next_song(self):
        if self.added_queue.qsize != 0:
            return self.added_queue.get()

    def print_queue(self):
        for song, user in list(self.added_queue.queue):
            print("{}, submitted by {}".format(song, user))

class Group_Queue:
    def __init__(self):
        self.lobbies = []

    def create_lobby(self, user, name, password):
        lobby = Lobby(name, password, user)
        self.lobbies.append(lobby)

        return lobby

gq = Group_Queue()
u1 = User("Jeffrey Li", "summer2019")
l1 = gq.create_lobby(u1, "Kenton's Home", "Kenton's Password")
l1.add_song_to_queue(u1, "I Get Lonely")
l1.print_queue()