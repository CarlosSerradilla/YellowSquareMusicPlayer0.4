import os
import time
import threading
import pygame
import keyboard
from colorama import Fore, Style
from Timer import PlayTimer

# Variables globales
timer_thread = None
current_stop_event = None
current_pause_event = None

def PlayTimer(duracion_total, stop_event, pause_event):
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
            print(f"\r{minutos:2d}:{segundos:02d} / {minutos_totales}:{segundos_totales:02d} {barra} ({porcentaje:.0%})", end="", flush=True)
            
            if stop_event.wait(1):
                return
            pause_event.wait()
        minutos += 1

def detener_timer_actual():
    global timer_thread, current_stop_event, current_pause_event
    
    if current_stop_event:
        current_stop_event.set()
    
    if timer_thread and timer_thread.is_alive():
        timer_thread.join(timeout=0.5)
    
    timer_thread = None
    current_stop_event = None
    current_pause_event = None

def iniciar_nuevo_timer(duracion_total):
    global timer_thread, current_stop_event, current_pause_event
    
    # Detener el timer anterior completamente
    detener_timer_actual()
    
    # Crear nuevos eventos para el nuevo timer
    current_stop_event = threading.Event()
    current_pause_event = threading.Event()
    current_pause_event.set()  # Comienza no pausado
    
    # Crear y lanzar el nuevo hilo
    timer_thread = threading.Thread(
        target=PlayTimer, 
        args=(duracion_total, current_stop_event, current_pause_event),
        daemon=True
    )
    timer_thread.start()

def pausar_timer():
    if current_pause_event:
        current_pause_event.clear()

def reanudar_timer():
    if current_pause_event:
        current_pause_event.set()

def PlaySoundtrack(folder, soundtrack_name):
    global current_pause_event
    
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
    
    print("")
    print(f"Now playing: {Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL}")
    print("  <- key  | spacebar | ⬆ key | escape | -> key")
    print(" previous |  pause   | loop  |  exit  |  next ")
    
    # Iniciar el timer para esta canción
    iniciar_nuevo_timer(duracion_total)
    
    while True:
        evento = keyboard.read_event()
        if evento.event_type == keyboard.KEY_UP:
            if evento.name == "space":
                if paused == False:
                    pygame.mixer.music.pause()
                    pausar_timer()
                    paused = True
                elif paused == True:
                    pygame.mixer.music.unpause()
                    reanudar_timer()
                    paused = False
            
            elif evento.name == "flecha arriba":
                detener_timer_actual()
                loop_enabled = not loop_enabled
                pygame.mixer.music.play(loops=-1 if loop_enabled else 0)
                iniciar_nuevo_timer(duracion_total)
                print(f"Loop {'enabled' if loop_enabled else 'disabled'}")
            
            elif evento.name == "flecha izquierda":
                detener_timer_actual()
                pygame.mixer.music.stop()
                return "previous"
            
            elif evento.name == "flecha derecha":
                detener_timer_actual()
                pygame.mixer.music.stop()
                return "next"
            
            elif evento.name == "esc":
                detener_timer_actual()
                pygame.mixer.music.stop()
                return "exit"