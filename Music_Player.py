from tkinter import * #graphic ui
import pygame
import os

root = Tk()
root.title("My Music")
root.geometry("500x300")

pygame.mixer.init() #initialise the audio functions


Song_list = Listbox(root,bg = "black",fg="white",width=100,height=15)
Song_list.pack()

#buttons
play_button_image = PhotoImage(file ="Play.png")
pause_button_image = PhotoImage(file ="Pause.png")
next_button_image = PhotoImage(file ="Next.png")
previous_button_image = PhotoImage(file ="Previous.png")


#frames
control_frame = Frame(root)
control_frame.pack()

play_button = Button (control_frame,image=play_button_image,borderwidth=10,width=60,height=50)
pause_button = Button (control_frame,image=pause_button_image,borderwidth=10,width=60,height=50)
next_button = Button (control_frame,image=next_button_image,borderwidth=10,width=60,height=50)
previous_button = Button (control_frame,image=previous_button_image,borderwidth=10,width=60,height=50)

play_button.grid(row=0, column=1, padx=0.000001,pady=0.0000002)
pause_button.grid(row=0, column=2, padx=0.000001,pady=0.000002)
next_button.grid(row=0, column=3, padx=0.000001,pady=0.0000002)
previous_button.grid(row=0, column=0 , padx=0.000001,pady=0.0000002)

root.mainloop() #run the code
