import pygame
import random
#canal_sonido1 = pygame.mixer.Channel(1)
#canal_sonido2 = pygame.mixer.Channel(2)

#canal_sonido1.play(musica_menu)
footstep_sounds = []
sound_queue = []  

def init_sounds():
    global footstep_sounds, sound_queue
    footstep_sounds = [
        pygame.mixer.Sound("assets/sounds/player/run/Dirt Run 1.wav"),
        pygame.mixer.Sound("assets/sounds/player/run/Dirt Run 2.wav"),
        pygame.mixer.Sound("assets/sounds/player/run/Dirt Run 3.wav"),
        pygame.mixer.Sound("assets/sounds/player/run/Dirt Run 4.wav"),
        pygame.mixer.Sound("assets/sounds/player/run/Dirt Run 5.wav"),
    ]
    for sound in footstep_sounds:
        sound.set_volume(0.2)


    sound_queue = footstep_sounds[:]
    random.shuffle(sound_queue)

def sonido_run():
    global sound_queue
    if not sound_queue:  
        sound_queue = footstep_sounds[:]
        random.shuffle(sound_queue)
    sound = sound_queue.pop(0)
    sound.play()


def sonido_menu():
    sonido = pygame.mixer.Sound("assets/sounds/pages.wav")
    sonido.set_volume(0.15)
    sonido.play()

def sonido_botones():
    sonido = pygame.mixer.Sound("assets/sounds/buttons.wav")
    sonido.set_volume(0.15)
    sonido.play()


def sonido_jump():
    sonido = pygame.mixer.Sound("assets/sounds/player/jump.wav")
    sonido.set_volume(0.15)
    sonido.play()

def sonido_land():
    sonido = pygame.mixer.Sound("assets/sounds/player/land.wav")
    sonido.set_volume(0.10)
    sonido.play()

def reproducir_musica_menu():
    pygame.mixer.music.load("assets/music/back_menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)