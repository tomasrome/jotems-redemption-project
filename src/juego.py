
import pygame
from config.screen import screen
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

    jugador = Player(100,631)
    enemigo_1 = Skeleton(900, 631)

    mover_izquierda= False
    mover_derecha = False

    ene_mover_izquierda= False
    ene_mover_derecha = False

    while corriendo:

        
        teclas = pygame.key.get_pressed()
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
                    if event.key == pygame.K_w:
                        mover_arriba = True
                    if event.key == pygame.K_d:
                        mover_derecha = True
                    if event.key == pygame.K_RIGHT:
                        ene_mover_derecha = True
                    if event.key == pygame.K_LEFT:
                        ene_mover_izquierda = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                if event.key == pygame.K_w:
                    mover_arriba = False
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

        if teclas[pygame.K_w]:
            jugador.saltar()
        
        if ene_mover_izquierda == True:
            delta_ene = -constantes.VELOCIDAD
            enemigo_1.movimiento(delta_ene)
        if ene_mover_derecha == True:
            delta_ene = constantes.VELOCIDAD
            enemigo_1.movimiento(delta_ene)

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jugador.atacar()
        if keys[pygame.K_UP]:
            enemigo_1.atacar()
        
        if jugador.atacando and jugador.forma.colliderect(enemigo_1.forma):
            enemigo_1.recibir_golpe()

        

        #Pausamos el movimiento del fondo
        #if jugador.forma.midbottom > (275,365) and jugador.estado != "idle":

          #  posicion_fondo_1 -= 2.5
          #  posicion_fondo_2 -= 3.5
          #  posicion_fondo_luces -= 1
        
        #if jugador.forma.midbottom < (20,365):

          #  posicion_fondo_1 += 2
          #  posicion_fondo_2 += 3
          #  posicion_fondo_luces += 1

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
        jugador.controlar_estado(teclas)
        jugador.updates()   
        jugador.dibujar(screen)

        enemigo_1.controlar_estado(teclas)
        enemigo_1.update()
        enemigo_1.dibujar(screen)

        pygame.display.flip()