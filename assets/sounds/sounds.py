import pygame

#canal_sonido1 = pygame.mixer.Channel(1)
#canal_sonido2 = pygame.mixer.Channel(2)

#canal_sonido1.play(musica_menu)

def sonido_menu():
    sonido = pygame.mixer.Sound("assets/sounds/pages.wav")
    sonido.set_volume(0.15)
    sonido.play()


def reproducir_musica_menu():
    pygame.mixer.music.load("assets/music/back_menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)