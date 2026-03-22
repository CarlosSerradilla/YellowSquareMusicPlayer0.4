import os
import pygame
import keyboard
from colorama import Fore, Style

def PlaySoundtrack(folder, soundtrack_name):

    file_path = os.path.join(folder, soundtrack_name)
    paused = False
    loop_enabled = False

    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "ERR0R! File not found" + Style.RESET_ALL)
        return "exit"
    
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(loops=-1 if loop_enabled else 0)
    name, _ = os.path.splitext(soundtrack_name)
    status = "looping" if loop_enabled else "not looping"
    print(f"Now playing: {Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL} ({status})")

    while True:
        evento = keyboard.read_event()
        if evento.event_type == keyboard.KEY_UP:
            if evento.name == "space":
                if not paused:
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    pygame.mixer.music.unpause()
                    paused = False

            if evento.name == "flecha arriba":
                loop_enabled = not loop_enabled
                pygame.mixer.music.play(loops=-1 if loop_enabled else 0)

            if evento.name == "flecha izquierda":
                pygame.mixer.music.stop()
                return "previous"

            if evento.name == "flecha derecha":
                pygame.mixer.music.stop()
                return "next"

            if evento.name == "esc":
                pygame.mixer.music.stop()
                return "exit"