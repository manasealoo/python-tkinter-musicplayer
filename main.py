import os
import time
import threading
from pygame import mixer
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from mutagen.mp3 import MP3

# from back import *


root = ThemedTk(theme="black")

root.title("AfroBit")
root.iconbitmap(r"icons/afrobit.ico")
root.configure(background="brown")

# initialize mixer
mixer.init()

paused = False  # for pausing and unpause song

# browse file to play
def browse_file():
    """opens a music file
    """
    global filename
    filename = filedialog.askopenfilename()
    add_song(filename)  # add browsed files to playlist


# play song
# filename = r"icons/137.FRANCO - Namiswi Misapi.mp3"


def play_song():
    """
    play selected song and unpause song
    """
    global filename
    global paused
    if paused:
        mixer.music.unpause()
        statusbar["text"] = f"playing {os.path.basename(filename)}"
        paused = False
    else:
        mixer.music.load(filename)
        mixer.music.play()
        statusbar["text"] = f"playing {os.path.basename(filename)}"
    show_song_status()


# stop song
def stop_song():
    mixer.music.stop()


def pause_song():
    """pause song being played
    """
    global paused
    paused = True
    mixer.music.pause()
    statusbar["text"] = f"Paused {os.path.basename(filename)}"


# rewind song
def rewind_song():
    mixer.music.rewind()
    statusbar["text"] = f"Rewinding {os.path.basename(filename)}"


# get song length
def show_song_status():
    # get the length of the song if mp3
    if filename.endswith(".mp3"):
        data = MP3(filename)
        totallength = data.info.length
    else:
        totallength = mixer.Sound.get_length(filename)
    mins, secs = divmod(totallength, 60)
    min1 = round(mins)
    sec = round(secs)
    timeformat = "{:02d}:{:02d}".format(min1, sec)
    totallabel["text"] = f"total length {timeformat}"
    # thread to manage current time
    t = threading.Thread(target=current_time, args=(totallength,))
    t.start()


# get current song time
def current_time(t):
    while t and mixer.music.get_busy():
        global paused  # to stop time when paused and resume when unpause
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            min1 = round(mins)
            sec = round(secs)
            timeformat = "{:02d}:{:02d}".format(min1, sec)
            currentlable["text"] = f"current time {timeformat}"
            time.sleep(1)
            t -= 1


def setvolume(val):
    """sets and controls music volume

    Arguments:
        val {[str]} -- [value from volume scale]

    Returns:
        [int] -- [sets the volume]
    """
    vol = float(val) / 100
    # mixer volume range between 0.1-1.0
    mixer.music.set_volume(vol)


# mute song
muted = False


def mute_song():
    global muted
    if muted:
        scale.set(70)
        mixer.music.set_volume(0.7)
        volume.configure(image=volumephoto)
        muted = False
    else:
        scale.set(0)
        mixer.music.set_volume(0)
        volume.configure(image=mutephoto)
        muted = True


# about afrobit
def about():
    return messagebox.showinfo("About", "AfroBit is a music app built using tkinter")


# add song to playlist
def add_song(f):
    """takes a file to be added to playlist

    Args:
        f ([str]): [sound object]
    """
    playlist.insert(1, os.path.basename(f))


# menu
submenu = Menu(root)
root.config(menu=submenu)
filemenu = Menu(submenu, tearoff=0, bg="brown")
submenu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="open file", command=browse_file)
filemenu.add_command(label="exit", command=root.destroy)
aboutus = Menu(submenu, tearoff=0, bg="brown")
submenu.add_cascade(label="About", menu=aboutus)
aboutus.add_command(label="About us", command=about)

statusbar = Label(
    root,
    text="Welcome to AfroBit",
    font="monospace 12 italic",
    anchor="w",
    background="brown",
    padx=3,
    pady=3,
)
statusbar.pack(side="bottom", fill="x")
# 2 frames for the interfaces
# left frame
left = ttk.Frame(root)
listlable = ttk.Label(left, text="play list", font="monospace 10 normal")
listlable.pack(side="top", anchor="w", padx=50, pady=5)
playlist = Listbox(left)
playlist.insert(0, "song1")
playlist.pack(padx=0)
# add and delete button
addlable = ttk.Button(left, text="+add music", command=browse_file)
addlable.pack(side="left", padx=10, pady=10)
dellable = ttk.Button(left, text="-del music")
dellable.pack(side="left", padx=10, pady=10)
left.pack(side="left", padx=10, pady=20)

# right frame
right = ttk.Frame(root)
# 3 frames,top,middle,bottom
# top frame
topframe = ttk.Frame(right)
# display music info
totallabel = ttk.Label(topframe, text="total length --:--")
totallabel.grid(row=0, column=0, padx=15, pady=15)

currentlable = ttk.Label(topframe, text="current time --:--")
currentlable.grid(row=0, column=1, padx=15, pady=15)
topframe.pack(padx=10, pady=15)

right.pack(side="left", padx=30, pady=20)

# middle frame ---todo
middleframe = ttk.Frame(right)
# control photos
playphoto = PhotoImage(file="icons/play.png")
pausephoto = PhotoImage(file="icons/pause.png")
stopphoto = PhotoImage(file="icons/stop-button.png")
rewindphoto = PhotoImage(file="icons/rewind.png")
nextphoto = PhotoImage(file="icons/next.png")

# button controls
play_ = ttk.Button(middleframe, image=playphoto, command=play_song)
play_.grid(row=0, column=0, padx=15, pady=15)
pause = ttk.Button(middleframe, image=pausephoto, command=pause_song)
pause.grid(row=0, column=1, padx=15, pady=15)
stop = ttk.Button(middleframe, image=stopphoto, command=stop_song)
stop.grid(row=0, column=2, padx=15, pady=15)
rewind = ttk.Button(middleframe, image=rewindphoto, command=rewind_song)
rewind.grid(row=0, column=3, padx=15, pady=15)
next_ = ttk.Button(middleframe, image=nextphoto)
next_.grid(row=0, column=4, padx=15, pady=15)


middleframe.pack()
# bottom frame
bottom = ttk.Frame(right)
# bottom photos
volumephoto = PhotoImage(file="icons/control-button.png")
mutephoto = PhotoImage(file="icons/silent.png")
# volume control buttons
volume = ttk.Button(bottom, image=volumephoto, command=mute_song)
volume.grid(row=0, column=0, padx=15, pady=15)
# volume scale
scale = ttk.Scale(bottom, from_=0, to=100, orient="horizontal", command=setvolume)
scale.grid(row=0, column=1, padx=15, pady=15)
scale.set(70)
mixer.music.set_volume(0.7)
bottom.pack(side="bottom")
root.mainloop()
