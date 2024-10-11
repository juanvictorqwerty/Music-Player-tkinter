def Slide(x): 
    global song_lenght3

    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.stop()  # Stop the music

    current_song = song_box.get(song_box.curselection()[0])
    current_song_path = os.path.join(os.path.dirname(root.filenames[0]), current_song)  # get the full path to the file
    pygame.mixer.music.load(current_song_path)  # load the music file using the path
    pygame.mixer.music.play(loops=0, start=int(slider.get()))  # Start playing from the new position

    current_song_index = song_box.curselection()[0]
    song_path = root.filenames[current_song_index]
    song_mutagen = MP3(song_path)
    song_lenght3 = song_mutagen.info.length
    slider.config(to=song_lenght3)  # Update the slider's maximum value
    slider_label.config(text=f"{int(slider.get())} of {song_lenght3}")
