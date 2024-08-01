from tkinter import filedialog
from tkinter import * #graphic ui
import pygame
import os

root = Tk()
root.title("My Music")
root.geometry("500x320")

pygame.mixer.init() #initialise the audio functions
menu_bar = Menu(root)
root.config(menu = menu_bar)

songs = []
current_song =""
paused = False

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


def Play_Music():
    global current_song ,paused

    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory,current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = True

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
        Play_Music()
    except:
        pass


def Previous_Music():
    global current_song,paused
    try:
        song_list.selection_clear(0,END)
        song_list.selection_set(songs.index(current_song)-1)
        current_song = songs[song_list.curselection()[0]]
        Play_Music()
    except:
        pass



organise_menu = Menu(menu_bar)
organise_menu.add_command(label=">>Select the folder DJ<<",command= Load_Music)
menu_bar.add_cascade(label="Organise",menu=organise_menu)

song_list = Listbox(root,bg = "black",fg="white",width=100,height=15)
song_list.pack()


play_button_image = PhotoImage(file ="Play.png")
pause_button_image = PhotoImage(file ="Pause.png")
next_button_image = PhotoImage(file ="Next.png")
previous_button_image = PhotoImage(file ="Previous.png")


#frames
control_frame = Frame(root)
control_frame.pack()

play_button = Button (control_frame,image=play_button_image,borderwidth=10,width=60,height=50,command=Play_Music)
pause_button = Button (control_frame,image=pause_button_image,borderwidth=10,width=60,height=50,command=Pause_Music)
next_button = Button (control_frame,image=next_button_image,borderwidth=10,width=60,height=50,command=Next_Music)
previous_button = Button (control_frame,image=previous_button_image,borderwidth=10,width=60,height=50,command=Previous_Music)

play_button.grid(row=0, column=1, padx=2,pady=2)
pause_button.grid(row=0, column=2, padx=2,pady=2)
next_button.grid(row=0, column=3, padx=2,pady=2)
previous_button.grid(row=0, column=0 , padx=2,pady=2)

root.mainloop() #run the code
