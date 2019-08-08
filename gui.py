from tkinter import *
import tkinter.messagebox as messagebox

class Group_Queue_Gui(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)
        self.spotify_username = 'Insert Spotify Username'

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def set_user_information(self, username):
        self.spotify_username = username

class LoginFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.label_username = Label(self, text='Username')
        self.label_password = Label(self, text='Password')

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show='*')

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)

        if username == "john" and password == "password":
            self.master.switch_frame(HomePage)
        else:
            messagebox.showerror("Login error", "Incorrect username")

class HomePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) 

        self.logoutbutton = Button(self, text='Logout', command=lambda: master.switch_frame(LoginFrame))
        self.logoutbutton.grid(row=0, column=0)

        self.homebutton = Button(self, text='Homepage', command=lambda: master.switch_frame(HomePage))
        self.homebutton.grid(row=0, column=1)

        self.settingbutton = Button(self, text='Settings', command=lambda:master.switch_frame(Settings))
        self.settingbutton.grid(row=0, column=2)

        self.single_label = Label(self, text='logged in successfully')
        self.single_label.grid(row=1, column=1)

class Settings(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.logoutbutton = Button(self, text='Logout', command=lambda: master.switch_frame(LoginFrame))
        self.logoutbutton.grid(row=0, column=0)

        self.homebutton = Button(self, text='Homepage', command=lambda: master.switch_frame(HomePage))
        self.homebutton.grid(row=0, column=1)

        self.settingbutton = Button(self, text='Settings', command=lambda: master.switch_frame(Settings))
        self.settingbutton.grid(row=0, column=2)

        self.username_label = Label(self, text='Spotify Username')
        self.username_label.grid(row=1, column=0)

        self.username_entry = Entry(self)
        self.username_entry.insert(END, master.spotify_username)
        self.username_entry.grid(row=1, column=1)


        self.set_button = Button(self, text='Set User Information', command=lambda: master.set_user_information(self.username_entry.get()))
        self.set_button.grid(row=2, column=1)

    # def set_user_information(self, master):
    #     master.spotify_username = self.username_entry.get()
    #     print("Spotify Username: {}".format(master.spotify_username))

        

if __name__ == "__main__":
    lf = Group_Queue_Gui()
    lf.mainloop()        























# import tkinter as tk
# from tkinter import *
# import Lyrical
# from tkinter import ttk


# def get_lyrics():
#     s_artists, s_name, s_album, s_lyrics = Lyrical.get_current_info()
#     name.config(text=s_name)
#     artists.config(text=str(s_artists))
#     album.config(text=s_album)
#     lyrics.delete('1.0', END)
#     lyrics.insert(INSERT, s_lyrics)
#     lyrics.tag_add('center', '1.0', 'end')

# root = tk.Tk()
# root.title("Lyrical")


# nb = ttk.Notebook(root)
# f1 = Frame(root, bg="black", width=500, height=500)
# f2 = Frame(root, bg='blue', width=500, height=500)
# nb.pack()
# nb.add(f1, text='Lyric Helper')
# nb.add(f2, text='Page 2')



# # Title widget
# ltitle = Label(f1, text='Lyrics', bg='black', fg='white')
# ltitle.grid(row=0, column=1)

# # Get info button
# get_button = Button(master=f1, text='Get Song Info', command=get_lyrics)
# get_button.grid(row=1, column=1)


# # Titles for response fields
# lname = Label(f1, text='Song Name:', bg='black', fg='white')
# lname.grid(row=2, column=0)
# lartists = Label(f1, text='Artist Name(s):', bg='black', fg='white')
# lartists.grid(row=3, column=0)
# lalbum = Label(f1, text='Album Name:', bg='black', fg='white')
# lalbum.grid(row=4, column=0)
# llyrics = Label(f1, text='Song Lyrics:', bg='black', fg='white')
# llyrics.grid(row=5, column=0, sticky=N)


# # Responses
# name = Label(f1, text='', bg='black', fg='white')
# name.grid(row=2, column=1)
# artists = Label(f1, text='', bg='black', fg='white')
# artists.grid(row=3, column=1)
# album = Label(f1, text='', bg='black', fg='white')
# album.grid(row=4, column=1)
# lyrics = Text(f1)
# lyrics.tag_configure('center', justify='center')
# lyrics.grid(row=5, column=1)






# root.mainloop()