from mutagen.mp3 import MP3 as mp3
import pygame  # required over python3.6
import time


def mp3_voice(mp3_file_path):
    mp3_file = mp3_file_path
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    mp3_length = mp3(mp3_file).info.length
    pygame.mixer.music.play(1)
    time.sleep(mp3_length + 0.25)
    pygame.mixer.music.stop()
