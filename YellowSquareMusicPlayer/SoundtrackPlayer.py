import os
import time
import threading
import pygame
import keyboard
from colorama import Fore, Style
from Timer import PlayTimer

stop_event = threading.Event()
pause_event = threading.Event()
pause_event.set()  # El hilo comienza en estado no pausado
timer_thread = None

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
    sonido = pygame.mixer.Sound(file_path)
    duracion_total = sonido.get_length()
    segundos_totales = duracion_total % 60
    minutos_totales = duracion_total // 60
    minutos = 0
    #status = "looping" if loop_enabled else "not looping"
    #status = "🔂" if loop_enabled else "🔀"
    print("")
    print(f"Now playing: {Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL}")
    print("  <- key  | spacebar | ⬆ key | escape | -> key")
    print(" previous |  pause   | loop  |  exit  |  next ")
    #print(f" Soundtrack duration: {minutos:2.0f}:{segundos:02.0f}") # :2.0f makes the code not showing the decimals

    # Lanzar el temporizador en segundo plano
    stop_event.clear()
    t = threading.Thread(target=PlayTimer, daemon=True)
    t.start()

    while True:
        evento = keyboard.read_event() #IMPORTANT: This should be change in case the device lenguage is other
        if evento.event_type == keyboard.KEY_UP:
            if evento.name == "space":
                if paused == False:
                    pygame.mixer.music.pause()
                    pausar()
                    paused = True
                elif paused == True:
                    pygame.mixer.music.unpause()
                    reanudar()
                    paused = False
                else:
                    print(Fore.LIGHTRED_EX + "ERR0R! How the fuck did you reach this error?" + Style.RESET_ALL)
            if evento.name == "flecha arriba":
                parar_timer()
                loop_enabled = not loop_enabled
                pygame.mixer.music.play(loops=-1 if loop_enabled else 0)
                status = "enabled" if loop_enabled else "disabled"
                iniciar_timer()
                print(f"Loop {status}")
            if evento.name == "flecha izquierda":
                parar_timer()
                pygame.mixer.music.stop()
                iniciar_timer()
                return "previous"
            if evento.name == "flecha derecha":
                parar_timer()
                pygame.mixer.music.stop()
                iniciar_timer()
                return "next"
            if evento.name == "esc":
                parar_timer()
                pygame.mixer.music.stop()
                return "exit"
            
def PlayTimer():
    minutos = 0
    while not stop_event.is_set():
        for i in range(60):
            print(f"\r{minutos}:{i:02d}", end="", flush=True)
            if stop_event.wait(1):  # ⬅️ instead sleep
                return
            pause_event.wait()  # ⬅️ waits here if the thread is paused
        minutos += 1

def pausar():
    pause_event.clear()  # pause the thread
def reanudar():
    pause_event.set()  # resume the thread

def iniciar_timer():
    global timer_thread
    stop_event.clear()
    timer_thread = threading.Thread(target=PlayTimer, daemon=True)
    timer_thread.start()
def parar_timer():
    global timer_thread
    stop_event.set()
    if timer_thread is not None:
        timer_thread.join()  # ⬅️ ESPERA a que muera el hilo