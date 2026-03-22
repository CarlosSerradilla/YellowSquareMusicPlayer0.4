import os # Interacts with the Operative System
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    # We hide the "Hello from the pygame community. https://www.pygame.org/contribute.html" pygame library support message at the start

# Libraries that we need to install: (python -m pip install)
import pygame # Has an audio mixer
import keyboard # For special keys like spacebar
import colorama
from colorama import Fore, Style, init
init()

    # FUNCTIONS:
def PlaySoundtrack(folder, soundtrack_name):

    file_path = os.path.join(folder, soundtrack_name)
    paused = False

    if not os.path.exists(file_path):
        print(Fore.LIGHTRED_EX + "ERR0R! File not found" + Style.RESET_ALL)
        return "exit"
    
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    name, _ = os.path.splitext(soundtrack_name)
    print(f"Now playing: {Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL}")
    print("  <- key  | spacebar | escape | -> key")
    print(" previous |  pause   |  exit  |  next ")

    while True:
        evento = keyboard.read_event() #IMPORTANT: This should be change in case the device lenguage is other
        if evento.event_type == keyboard.KEY_UP:
            if evento.name == "space":
                if paused == False:
                    pygame.mixer.music.pause()
                    paused = True
                elif paused == True:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    print(Fore.LIGHTRED_EX + "ERR0R! How the fuck did you reach this error?" + Style.RESET_ALL)
            if evento.name == "flecha izquierda":
                pygame.mixer.music.stop()
                return "previous"
            if evento.name == "flecha derecha":
                pygame.mixer.music.stop()
                return "next"
            if evento.name == "esc":
                pygame.mixer.music.stop()
                return "exit"

def main():
    try:
        pygame.mixer.init() # We initialize the music mixer
    except pygame.error as e:
        print(Fore.LIGHTRED_EX + "ERR0R! ", e + Style.RESET_ALL)
        return
    
    folder = "MusicExamples"

    if not os.path.isdir(folder):
        print(Fore.LIGHTRED_EX + f"ERR0R! Folder '{folder}' not found" + Style.RESET_ALL)
        print(Fore.LIGHTRED_EX + "You're now on",os.getcwd(),"route, try executing the script after moving to its route" + Style.RESET_ALL)
        return
    
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]
        # Only return the .mp3 files of the folder

    while True:
        if not mp3_files:
            print(Fore.LIGHTRED_EX + "ERR0R! Zero mp3 files found" + Style.RESET_ALL)
        else:
            print("My list:")
            print("0. Exit"+Fore.LIGHTYELLOW_EX)
            for index, soundtrack in enumerate(mp3_files, start=1): 
                name, _ = os.path.splitext(soundtrack) # We remove the .mp3 extension from the name of the soundtrack
                print(f"{index}. {name}")
        choice_input = input(Style.RESET_ALL+"Enter the soundtrack to play or 0 to Exit:")
        if choice_input == '0':
            print("Doing this thing...")
            break
        elif not choice_input.isdigit():
            print(Fore.LIGHTRED_EX + "ERR0R! Selecet a valid soundtrack" + Style.RESET_ALL)
            continue

        choice = int(choice_input)-1

        if 0 <= choice < len(mp3_files):
            current_index = choice
            while True:
                result = PlaySoundtrack(folder, mp3_files[current_index])
                if result == "next":
                    current_index = (current_index + 1) % len(mp3_files)
                elif result == "previous":
                    current_index = (current_index - 1) % len(mp3_files)
                elif result == "exit":
                    break
                else:
                    print(Fore.LIGHTRED_EX + "ERR0R! Invalid result from PlaySoundtrack" + Style.RESET_ALL)
                    break
        else:
            print(Fore.LIGHTRED_EX + "ERR0R! Invalid choice" + Style.RESET_ALL)

if __name__ == "__main__": #In case is import as module in other script
    main()