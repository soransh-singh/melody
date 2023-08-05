"""
    @author : Soransh singh
    These is going to be  a music player made in python
    using tkinter and (build with python)
    # root.iconbitnap(r'source/file.ico') to add icon
    #I made all the icons for the program
    <instead of obj.pack() we can use obj.grid() also>
    <I did not implememnted rewind button>
    there is an issue with current time ("<BIG ISSUES VERY BIG>")
    STRUCTURE:
    root
        |->rightFrame
        |    |->topFrame
        |    |    |->Label
        |    |->middleFrame
        |    |    |->button(All the four buttons)
        |    |->bottomFrame
        |         |->scale
        |->leftFrame
        |    |->listBox
        |    |->btn(add/del)song in playlist
        |
        |->statusBar
"""

import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading



# to setup a screen
root = tk.ThemedTk() # set up main screen

root.get_themes()
root.set_theme("plastik")

mixer.init() #initializing the mixer

#root.geometry('620x320') #set size of screen
root.title('melody') # set title of screen
root.iconbitmap(r'icons/icon.ico')

global paused
paused = False
# Creating and configuring menubar

playlist = []

def show_detail():
    file_data = os.path.splitext(filename)
    if file_data[1] == '.mp3':
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()
    mins,secs = divmod(total_length,60)#first variable contain value of quotient and another remainder
    mins = round(mins)
    secs = round(secs)
    timeformat = str(mins) + ':' + str(secs)
    lengthLabel['text'] = os.path.basename(filename) +' :: ' + timeformat
    t1 = threading.Thread(target = start_count, args = (total_length,))
    t1.start()


def start_count(t):
    global paused
    count = 0
    while count <= t and mixer.music.get_busy():
        if paused :
            continue
        else:
            mins,secs = divmod(count,60)#first variable contain value of quotient and another remainder
            mins = round(mins)
            secs = round(secs)
            timeformat = str(mins) + ':' + str(secs)
            currentLabel['text'] = os.path.basename(filename) +' :: ' + timeformat
            time.sleep(1)
            count += 1



def open_btn():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)
    add_to_playlist(filename)




def add_to_playlist(filePath):#f is the name of file with its path
    index =0
    file =os.path.basename(filePath)
    playlistBox.insert(index, file)
    playlist.insert(index, filePath)
    index += 1

def del_btn():
    selectedSong = playlistBox.curselection()
    selectedSong = int(selectedSong[0])
    playlist.remove(playlist[selectedSong])
    playlistBox.delete(selectedSong)


#to add button
def play_btn():
    try:
        global paused,filename
        if(paused):
            mixer.music.unpause()
            statusBar['text'] = 'Playing Music : '+ os.path.basename(filename)
            paused = False
        else:
            if(playlistBox.curselection()):
                selectedSong = playlistBox.curselection()
                selectedSong = int(selectedSong[0])
                filename = playlist[selectedSong]
            mixer.music.load(filename) #loading music
            mixer.music.play() #playing
            statusBar['text'] = 'Playing Music : '+ os.path.basename(filename)
            show_detail()
    except:
        statusBar['text'] ='File could not be found \n make sure you have opened the song'

def pause_btn():
    global paused
    paused = True
    mixer.music.pause()
    statusBar['text'] = 'Music paused : '+ os.path.basename(filename)


def stop_btn():
    mixer.music.stop()
    statusBar['text'] = 'Music stoped'
    currentLabel['text'] = 'current time :: --:--'

#scale widget. To set a volume
def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


mute = True
def mute_btn():
    global mute
    if(mute):
        muteBtn.configure(image = unmutePhoto)
        scale.set(0)
        mute = False
    else:
        muteBtn.configure(image = mutePhoto)
        scale.set(70)
        mute = True




menubar = Menu(root)
root.config(menu = menubar)

#creating a subMenu
subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'File', menu = subMenu)
subMenu.add_command(label = 'open', command = open_btn)
subMenu.add_command(label = 'exit', command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('melody','@author : Soransh singh \n These is a music player made in python using tkinter')

subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'help', menu = subMenu)
subMenu.add_command(label = 'about us', command = about_us)

#to add image

"""
photoLabel = Label(root, image = photo)
photoLabel.pack()
"""
statusBar = Label(root,text = 'Welcome to melody !!', relief = SUNKEN,  font = 'Times 12 bold')
statusBar.pack( anchor = W,side = BOTTOM)

rightFrame = Frame(root)
rightFrame.pack(side = RIGHT)

leftFrame = Frame(root)
leftFrame.pack(side = LEFT)
playlistBox = Listbox(leftFrame)
playlistBox.pack(pady = 10, padx = 30)



addBtn = ttk.Button(leftFrame, text = 'ADD', command = open_btn)
addBtn.pack(side = LEFT, padx = 10)
delBtn = ttk.Button(leftFrame, text = 'DEL', command = del_btn)
delBtn.pack(side = LEFT)
#to add a text
topFrame = Frame(rightFrame)
topFrame.pack(pady = 30)
title = Label(topFrame, text = 'music!!',font = 'Times 15 italic') #label
title.pack() #to add it on screen



lengthLabel = Label(topFrame,text = 'Song :: --:--',font = 'Times 10 italic')
lengthLabel.pack()

currentLabel = Label(topFrame,text = 'current time :: --:--',font = 'Times 10 italic')
currentLabel.pack()

middleFrame = Frame(rightFrame)
middleFrame.pack(pady = 30)


openPhoto = PhotoImage(file = 'icons/open.png')
openBtn = ttk.Button(middleFrame, image = openPhoto, command = open_btn)
openBtn.grid(row = 0, column = 0, padx = 10)


playPhoto = PhotoImage(file = 'icons/play.png')
playBtn = ttk.Button(middleFrame, image = playPhoto, command = play_btn)
playBtn.grid(row = 0, column = 1, padx = 10)



stopPhoto = PhotoImage(file = 'icons/stop.png')
stopBtn = ttk.Button(middleFrame, image = stopPhoto, command = stop_btn)
stopBtn.grid(row = 0, column = 2, padx = 10)



pausePhoto = PhotoImage(file = 'icons/pause.png')
pauseBtn = ttk.Button(middleFrame, image = pausePhoto, command = pause_btn)
pauseBtn.grid(row = 0, column = 3, padx = 10)

bottomFrame = Frame(rightFrame)
bottomFrame.pack(anchor = S,side=RIGHT,padx = 10)#pady = 30, expand = True

mutePhoto = PhotoImage(file = 'icons/mute.png')
unmutePhoto = PhotoImage(file = 'icons/unmute.png')
muteBtn = ttk.Button(bottomFrame, image = mutePhoto, command = mute_btn)
muteBtn.grid(row = 0, column = 0)


scale = ttk.Scale(bottomFrame, from_=0, to =100, orient = HORIZONTAL, command = set_vol)
scale.set(100) #set to default value you want
# mixer.music.set_volume(def) then set default value in it
scale.grid(row = 0, column = 1, columnspan = 5)





def on_closing():
    stop_btn()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop() # calls main screen in a loop
