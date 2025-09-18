import pygame
import src.utils.constantes as constantes
from src.entities.personaje import Personaje
from src.utils.funciones import mostrar_menu
from assets.sounds.sounds import reproducir_musica_menu, sonido_menu, init_sounds
from config.screen import boton_jugar,boton_salir
from src.juego import ejecutar_juego

pygame.init()
pygame.mixer.init()
init_sounds()
pygame.display.set_caption("Jotem´s Redemption")

reproducir_musica_menu()

run = True
reloj = pygame.time.Clock()

estado = "menu"

while run:

    reloj.tick(constantes.FPS)


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False

        if estado == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar.collidepoint(event.pos):
                sonido_menu()
                estado = "juego"
            if boton_salir.collidepoint(event.pos):
                sonido_menu()
                run = False


    if estado == "menu":
        mostrar_menu()
    elif estado == "juego":
        estado = ejecutar_juego()
    
    pygame.display.flip()

pygame.quit()