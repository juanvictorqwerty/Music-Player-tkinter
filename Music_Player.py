import random
from tkinter import filedialog
from tkinter import * #graphic ui
from mutagen.mp3 import MP3
import pygame
import os
import tkinter.ttk as ttk

root = Tk()
root.title("My Music")
root.geometry("500x380")

pygame.mixer.init() #initialise the audio functions
menu_bar = Menu(root)
root.config(menu = menu_bar)

songs = []
current_song =""
paused = False

current_song_label = Label(root, text="", font=("Arial", 12), wraplength=400)
current_song_label.pack()

def Load_Music():
    global current_song #so we can set it down
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name,extension = os.path.splitext(song)
        if extension == ".mp3":
            songs.append(song)

    for song in songs:
        song_list.insert("end",song)

    song_list.selection_set(0)
    current_song = songs[song_list.curselection()[0]]   
    song_list.selection_set(0)
    current_song_label.config(text=current_song)  # update the label 

def Play_Selected_Music(event):
    global current_song
    current_song = song_list.get(song_list.curselection()[0])
    current_song_label.config(text=current_song)  # update the label
    Play_Music()

def Play_Time():
    global song_lenght
    current_time = pygame.mixer.music.get_pos() / 1000  # convert milliseconds to seconds
    
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    time_str = f"{minutes:2d}:{seconds:2d}"  # format as MM:SS
    song_lenght = pygame.mixer.music.get_pos() / 1000  # update song_lenght in real-time
    status_bar.config(text=f" {time_str} / {int(song_lenght // 60):02d}:{int(song_lenght % 60):02d} ")
    status_bar.after(1000, Play_Time)  # update every 1 second
    

def Play_Music():
    global current_song, paused, song_lenght

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

    song_path = os.path.join(root.directory, current_song)
    song_mutagen = MP3(song_path)
    song_lenght = song_mutagen.info.length
    slider.config(to=int(song_lenght), value=0)
    song_list.selection_set(0)
    current_song_label.config(text=current_song)  # update the label

    Play_Time()


def Pause_Music():
    global pause
    pygame.mixer.music.pause()
    paused = True


def Next_Music():
    global current_song,paused

    try:
        song_list.selection_clear(0,END)
        song_list.selection_set(songs.index(current_song)+1)
        current_song = songs[song_list.curselection()[0]]
        song_list.selection_set(0)
        current_song_label.config(text=current_song)  # update the label
        Play_Music()
    except:
        pass


def Previous_Music():
    global current_song,paused
    try:
        song_list.selection_clear(0,END)
        song_list.selection_set(songs.index(current_song)-1)
        current_song = songs[song_list.curselection()[0]]
        song_list.selection_set(0)
        current_song_label.config(text=current_song)  # update the label
        Play_Music()
    except:
        pass

def Random():
    global songs,current_song
    random.shuffle(songs)
    song_list.delete(0, END)
    for song in songs:
        song_list.insert("end", song)
    
    song_list.selection_set(0)
    current_song_label.config(text=current_song)  # update the label
    current_song=songs[0]
    song_list.selection_set(0)
    Play_Music()
    Play_Time()

def Slide(x):
    global song_lenght
    pygame.mixer.music.play(start=float(x))
    slider.config(value=float(x))
    status_bar.config(text=f"{int(float(x) // 60):02d}:{int(float(x) % 60):02d} / {int(song_lenght // 60):02d}:{int(song_lenght % 60):02d}")


def Autoplay_Next(event):
    global current_song, paused
    try:
        song_list.selection_clear(0, END)
        current_index = songs.index(current_song)
        if current_index < len(songs) - 1:
            song_list.selection_set(current_index + 1)
            current_song = songs[song_list.curselection()[0]]
            Play_Music()
        else:
            song_list.selection_set(0)
            current_song = songs[song_list.curselection()[0]]
            Play_Music()
    except:
        pass

organise_menu = Menu(menu_bar)
organise_menu.add_command(label=">>Select the folder DJ<<",command= Load_Music)
menu_bar.add_cascade(label="Select",menu=organise_menu)

song_list = Listbox(root,bg = "black",fg="white",width=100,height=15)
song_list.pack()



#frames
control_frame = Frame(root)
control_frame.pack()

play_button = Button (control_frame,text= "PLAY",borderwidth=5,width=10,height=1,bg="MintCream",command=Play_Music)
pause_button = Button (control_frame,text="PAUSE",borderwidth=5,width=10,height=1,bg="MintCream",command=Pause_Music)
next_button = Button (control_frame,text="NEXT",borderwidth=5,width=10,height=1,bg="orange",command=Next_Music)
previous_button = Button (control_frame,text="PREVIOUS",borderwidth=5,width=10,height=1,bg="orange",command=Previous_Music)
random_button = Button (control_frame,text= "RANDOM",borderwidth=5,width=10,height=1,bg="SkyBlue",command= Random)

#grid
previous_button.grid(row=0, column=0 , padx=2,pady=2)
play_button.grid(row=0, column=1, padx=2,pady=2)
pause_button.grid(row=0, column=2, padx=2,pady=2)
next_button.grid(row=0, column=3, padx=2,pady=2)
random_button.grid(row=0,column=4,padx=2,pady=2)



#create status bar
status_bar = Label(root, text="",bd=1, relief=GROOVE, anchor=E )                                                 
status_bar.pack(fill=X,side=BOTTOM,ipady=4)

slider=ttk.Scale(root,from_=0, to=200, orient=HORIZONTAL,value=0,length=400,command=Slide)
slider.pack(fill=X,pady=30)
root.bind(pygame.USEREVENT + 1, Autoplay_Next)
song_list.bind("<<ListboxSelect>>", Play_Selected_Music)

root.mainloop() #run the code