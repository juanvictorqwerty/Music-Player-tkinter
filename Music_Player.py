from tkinter import * #graphic ui
import pygame
import os

root = Tk()
root.title("My Music")
root.geometry("900x600")

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

play_button = Button (control_frame,image=play_button_image,borderwidth=0,width=200,height=100)
pause_button = Button (control_frame,image=pause_button_image,borderwidth=0,width=200,height=100)
next_button = Button (control_frame,image=next_button_image,borderwidth=0,width=0,height=100)
previous_button = Button (control_frame,image=previous_button_image,borderwidth=0,width=200,height=100)

play_button.grid(row=0, column=1, padx=1,pady=2)
pause_button.grid(row=0, column=2, padx=1,pady=2)
next_button.grid(row=0, column=3, padx=1,pady=2)
previous_button.grid(row=0, column=0 , padx=2,pady=2)

root.mainloop() #run the code
