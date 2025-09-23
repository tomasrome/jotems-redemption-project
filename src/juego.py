import pygame
from src.config.screen import screen
import src.utils.constantes as constantes
from src.entities.personaje import Personaje
from src.utils.funciones import escalar_img
from src.entities.player import Player
from src.entities.skeleton import Skeleton


def ejecutar_juego():

    reloj = pygame.time.Clock()
    corriendo = True

    imagen_background_1 = pygame.image.load("assets//image//background//fondo10.png")
    posicion_fondo_1 = 0
    imagen_background_2 = pygame.image.load("assets//image//background//fondo20.png")
    posicion_fondo_2 = 0
    imagen_background_luces = pygame.image.load("assets//image//background//luces1.png")
    posicion_fondo_luces = 0

    jugador = Player(300,631)
    posicion_absoluta_jugador = 0 

    # Posición inicial del enemigo en pantalla
    posicion_inicial_enemigo_pantalla = 900
    # Posición absoluta del enemigo en el mundo (inicialmente igual a la de pantalla)
    posicion_absoluta_enemigo = posicion_inicial_enemigo_pantalla
    enemigo_1 = Skeleton(posicion_inicial_enemigo_pantalla, 631)
    # Establecer la posición absoluta inicial del enemigo
    enemigo_1.establecer_posicion_absoluta(posicion_absoluta_enemigo)

    mover_izquierda= False
    mover_derecha = False

    ene_mover_izquierda= False
    ene_mover_derecha = False

    while corriendo:

        keys = pygame.key.get_pressed()
        reloj.tick(constantes.FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        corriendo = False
                        return "menu"
                    if event.key == pygame.K_a:
                        mover_izquierda = True
                    if event.key == pygame.K_d:
                        mover_derecha = True
                    if event.key == pygame.K_RIGHT:
                        ene_mover_derecha = True
                    if event.key == pygame.K_LEFT:
                        ene_mover_izquierda = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_d:
                    mover_derecha = False
                if event.key == pygame.K_RIGHT:
                    ene_mover_derecha = False
                if event.key == pygame.K_LEFT:
                    ene_mover_izquierda = False

        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = constantes.VELOCIDAD
            jugador.movimiento(delta_x)
        if mover_izquierda == True:
            delta_x = -constantes.VELOCIDAD
            jugador.movimiento(delta_x)

        # Movimiento del enemigo (actualiza su posición absoluta)
        if ene_mover_izquierda == True:
            delta_ene = -constantes.VELOCIDAD
            enemigo_1.movimiento(delta_ene)  # Esto ya actualiza tanto pos_x como posicion_absoluta_x
        if ene_mover_derecha == True:
            delta_ene = constantes.VELOCIDAD
            enemigo_1.movimiento(delta_ene)  # Esto ya actualiza tanto pos_x como posicion_absoluta_x

        if keys[pygame.K_w]:
            jugador.saltar()
        if keys[pygame.K_SPACE]:
            jugador.atacar()
        if keys[pygame.K_UP]:
            enemigo_1.atacar()

        hitbox = jugador.get_hitbox()
        if hitbox:
            pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)

        if hitbox and hitbox.colliderect(enemigo_1.forma):
            enemigo_1.recibir_golpe()

        # Variables para trackear el desplazamiento del fondo
        desplazamiento_fondo = 0

        # Pausamos el movimiento del fondo
        if jugador.forma.midbottom > (899,631) and jugador.estado != "idle":
            desplazamiento_fondo = -10.5
            posicion_fondo_1 -= 10.5
            posicion_fondo_2 -= 11.5
            posicion_fondo_luces -= 12
            posicion_absoluta_jugador += 10.5  

        if jugador.forma.midbottom < (200,631) and posicion_absoluta_jugador > 0:  
            desplazamiento_fondo = 10.5
            posicion_fondo_1 += 10.5
            posicion_fondo_2 += 11.5
            posicion_fondo_luces += 12
            posicion_absoluta_jugador -= 10.5  

        # Siempre sincronizar la posición del enemigo en pantalla con su posición absoluta
        # independientemente de si hay desplazamiento o no
        pos_absoluta_enemigo = enemigo_1.obtener_posicion_absoluta()
        nueva_posicion_pantalla = pos_absoluta_enemigo - posicion_absoluta_jugador + 300
        enemigo_1.actualizar_posicion_pantalla(nueva_posicion_pantalla)

        if posicion_fondo_1 <= -1280 or posicion_fondo_1 >= 1280:
            posicion_fondo_1 = 0

        if posicion_fondo_2 <= -1280 or posicion_fondo_2 >= 1280:
            posicion_fondo_2 = 0

        posicion_fondo_luces -= 1.3

        if posicion_fondo_luces <= -1280 or posicion_fondo_luces >= 1280:
            posicion_fondo_luces = 0

        screen.blit(imagen_background_1,(posicion_fondo_1,0))
        screen.blit(imagen_background_1,(posicion_fondo_1+1280,0))
        screen.blit(imagen_background_luces,(posicion_fondo_luces,0))
        screen.blit(imagen_background_luces,(posicion_fondo_luces+1280,0))
        screen.blit(imagen_background_2,(posicion_fondo_2,0))
        screen.blit(imagen_background_2,(posicion_fondo_2+1280,0))

        jugador.movimiento(delta_x)
        jugador.controlar_estado(keys)
        jugador.updates()   
        jugador.dibujar(screen)

        enemigo_1.controlar_estado(keys)
        enemigo_1.update()
        enemigo_1.dibujar(screen)

        pygame.display.flip()