import random
import pygame
import os
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import * #graphic ui
from mutagen.mp3 import MP3

root = Tk()
root.title("My Music")
root.geometry("510x380")

pygame.mixer.init() #initialise the audio functions
menu_bar = Menu(root)
root.config(menu = menu_bar)

global songs_list
songs_list = []
global current_song
current_song =""
global paused 
paused= False
file_path=[]
current_song_label = Label(root, text="", font=("Arial", 12), wraplength=400)
current_song_label.pack()

def Load_Music():
    global current_song #so we can set it down
    root.filenames = list(filedialog.askopenfilenames())

    for song in root.filenames:
        songs_list.append(os.path.basename(song))

    for song in songs_list:
        song_box.insert("end",song)
    
    song_box.selection_set(0)
    current_song = songs_list[song_box.curselection()[0]]
    Play_Music()
    song_box.selection_set(0)
    current_song_label.config(text=current_song)  # update the label
    

# def Play_Selected_Music(event):
#   global current_song
#   current_song = song_box.get(song_box.curselection()[0])
#   current_song_label.config(text=current_song)  # update the label
#   Play_Music()

def Play_Time():
    global song_lenght
    global current_time

    current_time = pygame.mixer.music.get_pos()/1000  # convert milliseconds to seconds
    print("CT",current_time)
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    converted_current_song = f"{minutes:2d}:{seconds:2d}"  # format as MM:SS
    
    current_song_index= song_box.curselection()[0]
    
    song_path = root.filenames[current_song_index]
    song_mutagen = MP3(song_path)
    song_lenght = song_mutagen.info.length
    

    status_bar.config(text=f" {converted_current_song} / {int(song_lenght// 60):02d}:{int(song_lenght % 60):02d} ")
    status_bar.after(1000, Play_Time)  # update every 1 second
    

def Pause_Music(is_paused):
    global paused

    if not paused: 
        paused=is_paused
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

def Play_Music():
    global  paused
    global song_lenght2

    if not paused:
        current_song = song_box.get(song_box.curselection()[0])
        current_song_path = os.path.join(os.path.dirname(root.filenames[0]), current_song)  # get the full path to the file
        pygame.mixer.music.load(current_song_path)  # load the music file using the path
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()


    current_song_index= song_box.curselection()[0]
    
    song_path = root.filenames[current_song_index]
    song_mutagen = MP3(song_path)
    song_lenght2 = song_mutagen.info.length    

    current_song_label.config(text=current_song)  # update the label
    Play_Time()

def Next_Music():
    global current_song,paused

    try:
        song_box.selection_clear(0,END)
        song_box.selection_set(songs_list.index(current_song)+1)
        current_song = songs_list[song_box.curselection()[0]]
        current_song_label.config(text=current_song)  # update the label
        Play_Music()
        Play_Time()
    except:
        pass


def Previous_Music():
    global current_song,paused
    try:
        song_box.selection_clear(0,END)
        song_box.selection_set(songs_list.index(current_song)-1)
        current_song = songs_list[song_box.curselection()[0]]
        current_song_label.config(text=current_song)  # update the label
        Play_Music()
        Play_Time()
    except:
        pass


def Random():
    global songs_list,current_song
    random.shuffle(songs_list)
    song_box.delete(0, END)
    for song in songs_list:
        song_box.insert("end", song)
    
    song_box.selection_set(0)
    current_song_label.config(text=current_song)  # update the label
    current_song=songs_list[0]
    song_box.selection_set(0)
    Play_Music()
    Play_Time()

def Jump_Forward():

    # Get the current time in seconds
    try:
        current_time = pygame.mixer.music.get_pos() // 1000  # get current position in seconds
        
        current_time = (current_time + 10)
        
        #pygame.mixer.music.pause()  # stop the current music
        pygame.mixer.music.set_pos(current_time) # play from the new position
        print(current_time)
        Play_Time()
    except:
        pass

def Jump_Backward():

    # Get the current time in seconds
    current_time = pygame.mixer.music.get_pos() / 1000  # get current position in seconds
    
    # Subtract 10 seconds from the current time
    new_time = current_time - 10
    
    # Ensure we don't jump before the start of the song
    if new_time < 0:
        new_time = 0
    
    # Jump to the new position
    pygame.mixer.music.play(loops=0, start=new_time)
    


Add_Songs_Menu = Menu(menu_bar)
Add_Songs_Menu.add_command(label=">>Select The Songs DJ<<",command= Load_Music)
menu_bar.add_cascade(label="Add Songs",menu=Add_Songs_Menu,activebackground="MintCream",activeforeground="black")

song_box = Listbox(root,bg = "black",fg="MintCream",width=100,height=15,selectbackground="green",selectforeground="white")
song_box.pack(fill="both",pady=1)



#frames
control_frame = Frame(root)
control_frame.pack(fill="both")

play_button = Button (control_frame,text= "PLAY",borderwidth=2,width=10,height=1,bg="MintCream",command=Play_Music)
pause_button = Button (control_frame,text="PAUSE",borderwidth=2,width=10,height=1,bg="MintCream",command=lambda:Pause_Music(paused))
next_button = Button (control_frame,text="NEXT",borderwidth=2,width=10,height=1,bg="orange",command=Next_Music)
previous_button = Button (control_frame,text="PREVIOUS",borderwidth=2,width=10,height=1,bg="orange",command=Previous_Music)
random_button = Button (control_frame,text= "RANDOM",borderwidth=2,width=10,height=1,bg="SkyBlue",command= Random)
jump_forward_button= Button(control_frame,text= "+10",borderwidth=2,width=10,height=1,bg="gray",command= Jump_Forward)
#grid
previous_button.grid(row=0, column=0 , padx=2,pady=1)
play_button.grid(row=0, column=1, padx=2,pady=1)
pause_button.grid(row=0, column=5, padx=2,pady=1)
next_button.grid(row=0, column=2, padx=2,pady=1)
random_button.grid(row=0,column=4,padx=2,pady=1)
jump_forward_button.grid(row=0,column=6,padx=2,pady=1)

#create status bar
status_bar = Label(root, text="",bd=1, relief=GROOVE, anchor=E )                                                 
status_bar.pack(fill=X,side=BOTTOM,ipady=2)



root.mainloop() #run the code