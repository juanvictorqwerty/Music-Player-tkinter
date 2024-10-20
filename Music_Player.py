import random
import pygame
import os
import tkinter as ttk
from tkinter import filedialog
from tkinter import * #graphic ui
from mutagen.mp3 import MP3



class Song:
    def __init__(self, filepath):
        self.filepath = filepath
        self.basename = os.path.basename(filepath)
        self.length = self.get_length()
        self.current_position = 0


    def get_length(self):
        audio = MP3(self.filepath)
        return audio.info.length


class MusicPlayer():
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x400")

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=8192)  # Initialize the mixer

        self.songs = []
        self.current_song_index = 0
        self.random=[]
        self.paused = False


        self.setup_ui()


    def setup_ui(self):
        self.setup_menu()
        self.setup_song_list()
        self.setup_controls()
        self.setup_status_bar()
        self.setup_slider()  # Add the slider setup


    def setup_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        add_songs_menu = Menu(menu_bar)
        add_songs_menu.add_command(label="Add Songs", command=self.load_music)
        menu_bar.add_cascade(label="File", menu=add_songs_menu)


    def setup_song_list(self):
        self.song_box = Listbox(self.root, bg="black", fg="white", width=60, height=15,
                                selectbackground="green", selectforeground="black")
        self.song_box.pack(fill='both')


    def setup_controls(self):
        control_frame = Frame(self.root)
        control_frame.pack()

        Button(control_frame, text="Play", command=self.play_music).grid(row=0, column=0, padx=5)
        Button(control_frame, text="Pause", command=self.toggle_pause).grid(row=0, column=1, padx=5)
        Button(control_frame, text="Next", command=self.next_music).grid(row=0, column=2, padx=5)
        Button(control_frame, text="Previous", command=self.previous_music).grid(row=0, column=3, padx=5)
        Button(control_frame, text="Random", command=self.Random).grid(row=0, column=4, padx=5)


    def setup_status_bar(self):
        self.current_song_label = Label(self.root, text="", font=("Arial", 12))
        self.current_song_label.pack(pady=10)


    def load_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file_path in file_paths:
            song = Song(file_path)
            self.songs.append(song)
            self.song_box.insert(END, song.basename)

        self.play_music()


    def play_music(self):

        if self.songs:
            current_song = self.songs[self.current_song_index]
            pygame.mixer.music.load(current_song.filepath)
            pygame.mixer.music.play()
            self.current_song_label.config(text=f"Playing: {current_song.basename} (Length: {int(current_song.length)}s)")

            self.slider.config(to=current_song.length)  # Set the slider max to song length
            self.update_slider()  # Start updating the slider position
            current_song_position = pygame.mixer.music.get_pos()
            print(current_song_position)
            self.position_label.config(text=f"{int(current_song_position)//60} : {int(current_song_position%60)} / {int(current_song.length)//60} : {int(current_song.length%60)} ")
            self.update_time_elapsed()


    def update_time_elapsed(self):
        if self.songs:
            current_song = self.songs[self.current_song_index]
            current_song_position = pygame.mixer.music.get_pos()

        if current_song_position == -1:  # If the song is not playing, get_pos() returns -1
            current_song_position = 0

        minutes = int(current_song_position // 60000)
        seconds = int((current_song_position % 60000) // 1000)

        self.position_label.config(text=f"{minutes}:{seconds:02d} / {int(current_song.length)//60} : {int(current_song.length%60):02d}")

        # Call the update_position method again after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_time_elapsed)

    def toggle_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        self.paused = not self.paused


    def next_music(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_music()


    def previous_music(self):
        self.current_song_index = (self.current_song_index -1) % len(self.songs)
        self.play_music()

    def Random(self):
        random.shuffle(self.songs)
        self.song_box.delete(0, END)
        for song in self.songs:
            self.song_box.insert("end", song.basename)
        self.current_song_index=0
        self.play_music()


    def setup_slider(self):
        self.slider = Scale(self.root, from_=0, to=100, orient='horizontal', command=self.seek_music)
        self.slider.pack(fill='x', ipady=2)

        # Create a label to display the current position and length
        self.position_label = Label(self.root,text="hello", font=("Arial", 10))
        self.position_label.pack(pady=5)

    def seek_music(self, value):
        """Seek to the position specified by the slider."""
        if self.songs:
            current_song = self.songs[self.current_song_index]
            try:
                pygame.mixer.music.set_pos(float(value))  # Seek to the selected position
            except Exception as e:
                print(f"Error seeking to position: {e}")


    def update_slider(self):
        if self.songs:
            current_song = self.songs[self.current_song_index]
            current_position = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds

            # Update the slider position
            self.slider.set(current_position)

            # Call this method again after 100 milliseconds (0.1 seconds)
            self.root.after(100, self.update_slider)

if __name__ == "__main__":
    root = ttk.Tk()
    player = MusicPlayer(root)
    root.mainloop()