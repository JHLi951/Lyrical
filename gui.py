import tkinter as tk
from tkinter import *
import Lyrical

def get_lyrics():
    s_artists, s_name, s_album, s_lyrics = Lyrical.get_current_info()
    name.config(text=s_name)
    artists.config(text=str(s_artists))
    album.config(text=s_album)
    lyrics.delete('1.0', END)
    lyrics.insert(INSERT, s_lyrics)
    lyrics.tag_add('center', '1.0', 'end')

m = tk.Tk()
m.title("Lyrical")

# Title widget
ltitle = Label(m, text='Lyrics')
ltitle.grid(row=0, column=1)

# Get info button
get_button = Button(master=m, text='Get Song Info', command=get_lyrics)
get_button.grid(row=1, column=1)


# Titles for response fields
lname = Label(m, text='Song Name:')
lname.grid(row=2, column=0)
lartists = Label(m, text='Artist Name(s):')
lartists.grid(row=3, column=0)
lalbum = Label(m, text='Album Name:')
lalbum.grid(row=4, column=0)
llyrics = Label(m, text='Song Lyrics:')
llyrics.grid(row=5, column=0, sticky=N)


# Responses
name = Label(m, text='')
name.grid(row=2, column=1)
artists = Label(m, text='')
artists.grid(row=3, column=1)
album = Label(m, text='')
album.grid(row=4, column=1)
lyrics = Text(m)
lyrics.tag_configure('center', justify='center')
lyrics.grid(row=5, column=1)

m.mainloop()