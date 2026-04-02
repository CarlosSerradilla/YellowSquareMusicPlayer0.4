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
    #status = "looping" if loop_enabled else "not looping"
    #status = "🔂" if loop_enabled else "🔀"
    print("")
    print(f"Now playing: {Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL}")
    print("  <- key  | spacebar | ⬆ key | escape | -> key")
    print(" previous |  pause   | loop  |  exit  |  next ")
   # Lanzar el temporizador en segundo plano
    stop_event.clear()
    pause_event.set()  # ← Importante: asegura que no empiece pausado
    t = threading.Thread(target=PlayTimer, args=(duracion_total,), daemon=True)
    t.start()
    timer_thread = t  # ← Guarda la referencia global

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
                iniciar_timer(duracion_total)
                print(f"Loop {status}")
            if evento.name == "flecha izquierda":
                parar_timer()
                pygame.mixer.music.stop()
                iniciar_timer(duracion_total)
                return "previous"
            if evento.name == "flecha derecha":
                parar_timer()
                pygame.mixer.music.stop()
                iniciar_timer(duracion_total)
                return "next"
            if evento.name == "esc":
                parar_timer()
                pygame.mixer.music.stop()
                return "exit"

# Probablemente debería meter esta función en otro Script lol    
def PlayTimer(duracion_total):
    minutos = 0
    minutos_totales = int(duracion_total // 60)
    segundos_totales = int(duracion_total % 60)
    ancho_barra = 30  # Ancho de la barra de progreso
    
    while not stop_event.is_set():
        for segundos in range(60):
            tiempo_transcurrido = minutos * 60 + segundos
            
            if tiempo_transcurrido > duracion_total:
                # Barra completa
                barra = "█" * ancho_barra
                print(f"\r{barra} {minutos:2d}:{segundos:02d} / {minutos_totales}:{segundos_totales:02d} [COMPLETADO]", end="", flush=True)
                return
            
            # Calcular porcentaje y barra de progreso
            porcentaje = tiempo_transcurrido / duracion_total
            filled = int(ancho_barra * porcentaje)
            barra = "█" * filled + "░" * (ancho_barra - filled)
            
            # Mostrar todo junto
            print(f"\r{barra} {minutos:2d}:{segundos:02d} / {minutos_totales}:{segundos_totales:02d} ({porcentaje:.0%})", end="", flush=True)
            
            if stop_event.wait(1):
                return
            pause_event.wait()
        minutos += 1

def pausar():
    pause_event.clear()  # pause the thread
def reanudar():
    pause_event.set()  # resume the thread

def iniciar_timer(duracion_total):
    global timer_thread
    stop_event.set()  # Asegura que el hilo anterior termine
    
    if timer_thread and timer_thread.is_alive():
        timer_thread.join(timeout=0.1)  # Espera a que muera
    
    stop_event.clear()
    pause_event.set()  # Asegura que el nuevo hilo no empiece pausado
    timer_thread = threading.Thread(target=PlayTimer, args=(duracion_total,), daemon=True)
    timer_thread.start()
def parar_timer():
    global timer_thread
    stop_event.set()
    if timer_thread and timer_thread.is_alive():
        timer_thread.join(timeout=0.5)  # Espera hasta medio segundo
    timer_thread = None