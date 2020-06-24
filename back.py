import os
from pygame import mixer
from tkinter import messagebox
from tkinter import filedialog

__all__ = ["browse_file", "setvolume", "play_song", "about", "pause_song"]
# initialize mixer

mixer.init()

# browse file to play
def browse_file():
    """opens a music file
    """
    song_ = filedialog.askopenfile()
    return song_


# selected song
# fileplay = browse_file
# play song


def play_song():
    """
    play selected song
    """
    filename = "icons/137.FRANCO - Namiswi Misapi.mp3"
    mixer.music.load(filename)
    mixer.music.play()


def pause_song():
    """pause song being played
    """
    mixer.music.pause()


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


# about afrobit
def about():
    return messagebox.showinfo("About", "AfroBit is a music app built using tkinter")
