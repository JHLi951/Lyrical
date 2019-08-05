import tkinter as tk
from tkinter import *
import Lyrical
from tkinter import ttk

def get_lyrics():
    s_artists, s_name, s_album, s_lyrics = Lyrical.get_current_info()
    name.config(text=s_name)
    artists.config(text=str(s_artists))
    album.config(text=s_album)
    lyrics.delete('1.0', END)
    lyrics.insert(INSERT, s_lyrics)
    lyrics.tag_add('center', '1.0', 'end')

root = tk.Tk()
root.title("Lyrical")


nb = ttk.Notebook(root)
f1 = Frame(root, bg="black", width=500, height=500)
f2 = Frame(root, bg='black', width=500, height=500)
nb.pack()
nb.add(f1, text='Lyric Helper')
nb.add(f2, text='Page 2')



# Title widget
ltitle = Label(f1, text='Lyrics', bg='black', fg='white')
ltitle.grid(row=0, column=1)

# Get info button
get_button = Button(master=f1, text='Get Song Info', command=get_lyrics)
get_button.grid(row=1, column=1)


# Titles for response fields
lname = Label(f1, text='Song Name:', bg='black', fg='white')
lname.grid(row=2, column=0)
lartists = Label(f1, text='Artist Name(s):', bg='black', fg='white')
lartists.grid(row=3, column=0)
lalbum = Label(f1, text='Album Name:', bg='black', fg='white')
lalbum.grid(row=4, column=0)
llyrics = Label(f1, text='Song Lyrics:', bg='black', fg='white')
llyrics.grid(row=5, column=0, sticky=N)


# Responses
name = Label(f1, text='', bg='black', fg='white')
name.grid(row=2, column=1)
artists = Label(f1, text='', bg='black', fg='white')
artists.grid(row=3, column=1)
album = Label(f1, text='', bg='black', fg='white')
album.grid(row=4, column=1)
lyrics = Text(f1)
lyrics.tag_configure('center', justify='center')
lyrics.grid(row=5, column=1)






root.mainloop()