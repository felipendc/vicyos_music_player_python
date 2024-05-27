# music_player.py
import vlc, os
import customtkinter as ctk


repeat_options = {
    "NONE": "none",
    "CURRENT": "current",
    "PLAYLIST": "playlist",
}


repeat_song = repeat_options["NONE"]
pause_music = False
stop_music = False
music_folder_path = []
song_index = 0


def init_music_player():
    # Creating VLC instance
    global instance, player
    instance = vlc.Instance()

    # Creating VLC media player
    player = instance.media_player_new()


def open_songs(filedialog, play_pause_button, stop_button, next_button, previous_button, is_play_button, repeat_button, select_folder_button):
    global music_folder_path, song_index

    dialog_title = "Select a Directory"
    initial_directory = os.path.expanduser("~/Music")
    supported_extensions = ["*.m4a*", "*.mp3*"]
    
    selected_songs = filedialog.askopenfilenames(
        initialdir=initial_directory,
        filetypes=[(".mp3", "*.mp3"), (".m4a", "*.m4a*"), ("All files", supported_extensions)],
        title=dialog_title
    )

    music_folder_path = selected_songs
    
    if len(music_folder_path) > 0:
        print(music_folder_path)
        song_index = 0
        on_button_stop(play_pause_button)
        on_button_play_or_pause(play_pause_button)
        play_pause_button.configure(state=ctk.NORMAL)
        stop_button.configure(state=ctk.NORMAL)
        next_button.configure(state=ctk.NORMAL)
        previous_button.configure(state=ctk.NORMAL)
        is_play_button.configure(state=ctk.NORMAL)
        repeat_button.configure(state=ctk.NORMAL)
        select_folder_button.configure(fg_color="#444444", hover_color="#555555",)
    else:
        pass


def open_folder(filedialog, play_pause_button, stop_button, next_button, previous_button, is_play_button, repeat_button, select_folder_button):
    global music_folder_path, song_index

    suported_files_extensions = [".mp3", ".m4a"]
    directory = filedialog.askdirectory()

    if directory:
        music_folder_path.clear()  # Empty the current playlist

        for root_, dirs, files in os.walk(directory):
            for file in files:
                for suported_extensions in suported_files_extensions:
                    print(suported_extensions)
                    if os.path.splitext(file)[1].lower() == suported_extensions:
                        path = (root_ + "/" + file).replace("\\", "/")
                        music_folder_path.append(path)
                    
        if len(music_folder_path) > 0:
            print(music_folder_path)
            song_index = 0
            on_button_stop(play_pause_button)
            on_button_play_or_pause(play_pause_button)
            play_pause_button.configure(state=ctk.NORMAL)
            stop_button.configure(state=ctk.NORMAL)
            next_button.configure(state=ctk.NORMAL)
            previous_button.configure(state=ctk.NORMAL)
            is_play_button.configure(state=ctk.NORMAL)
            repeat_button.configure(state=ctk.NORMAL)
            select_folder_button.configure(fg_color="#444444", hover_color="#555555",)
    else:
        pass

def next_song():
    global song_index
    if song_index < len(music_folder_path) - 1:
        song_index += 1
        media = instance.media_new(music_folder_path[song_index])
        player.set_media(media)
        player.play()
    elif song_index >= len(music_folder_path) - 1:
        song_index = 0
        media = instance.media_new(music_folder_path[song_index])
        player.set_media(media)
        player.play()


def previous_song():
    global song_index
    if song_index > 0:
        song_index -= 1
        media = instance.media_new(music_folder_path[song_index])
        player.set_media(media)
        player.play()
    else:
        song_index = 0

def on_button_play_or_pause(play_pause_button):
    global pause_music, music_folder_path, stop_music, instance
    if player.get_state() != vlc.State.Ended and pause_music == False:
        
        media = instance.media_new(music_folder_path[song_index])
        player.set_media(media)
        player.play()
        stop_music = False
        play_pause_button.configure(text="Pause")
    elif pause_music == False:
        player.pause()
        pause_music = True
        play_pause_button.configure(text="Play")
    elif pause_music == True:
        player.unpause()
        pause_music = False
        play_pause_button.configure(text="Pause")

def on_button_stop(play_pause_button):
    global pause_music, stop_music
    player.stop()
    pause_music = False
    stop_music = True
    play_pause_button.configure(text="Start Playing the song")

def check_music():
    global music_folder_path
    
    if player.get_state() == vlc.State.Ended and pause_music == False:
        print("There is nothing being played at the moment...")
    elif player.get_state() == vlc.State.Ended and pause_music == True:
        print("The song is currently paused!")
    else:
        print("There is a song being played at the moment...")


def repeat_checker(root, play_pause_button):
    global music_folder_path, repeat_song
    if player.get_state() == vlc.State.Ended and pause_music == False:
        if repeat_song == repeat_options["PLAYLIST"]:
            if len(music_folder_path) > 0 and not stop_music:
                next_song()
            print(repeat_song) # Printing to debug the code!
        elif repeat_song == repeat_options["CURRENT"]:
            if len(music_folder_path) > 0:
                media = instance.media_new(music_folder_path[song_index])
                player.set_media(media)
                player.play()
            print(repeat_song) # Printing to debug the code!
        elif repeat_song == repeat_options["NONE"]:
            if len(music_folder_path) > 0:
                play_pause_button.configure(text="Play")
                pass

            print(repeat_song) # Printing to debug the code!
    root.after(1000, lambda: repeat_checker(root, play_pause_button))
        

def repeat_button_label(repeat_button):
    global repeat_song
    if repeat_song == repeat_options["NONE"]:
        print(repeat_song) # Printing to debug the code!
        repeat_button.configure(text="Repeat: Current song")
        repeat_song = repeat_options["CURRENT"]
        print(repeat_song) # Printing to debug the code!
    elif repeat_song == repeat_options["CURRENT"]:
        print(repeat_song) # Printing to debug the code!
        repeat_button.configure(text="Repeat: Playlist")
        repeat_song = repeat_options["PLAYLIST"]
        print(repeat_song) # Printing to debug the code!
    elif repeat_song == repeat_options["PLAYLIST"]:
        print(repeat_song) # Printing to debug the code!
        repeat_button.configure(text="Repeat mode: Off")
        repeat_song = repeat_options["NONE"]
        print(repeat_song) # Printing to debug the code!