import pygame
from config.screen import boton_jugar,boton_opciones,boton_salir,screen
from assets.image.background.background import background_menu
from assets.color import color
import src.utils.constantes as constantes
from src.entities.personaje import Personaje
from assets.sounds.sounds import sonido_botones
import os

def dibujar_texto(texto, x, y, color, tamanio = 40):

    fuente_opciones = pygame.font.Font("assets/fonts/ForwardSerif_PERSONAL_USE_ONLY.otf", tamanio)
    superficie = fuente_opciones.render(texto,True,color)
    rect = superficie.get_rect()
    rect.center = (x,y)
    screen.blit(superficie,rect)
    return rect



def mostrar_menu():
    
    screen.blit(background_menu,(0,0))

    
    if boton_jugar.collidepoint(pygame.mouse.get_pos()):
        sonido_botones()
        pygame.draw.rect(screen,(245, 245, 245),boton_jugar)
        dibujar_texto("Play", boton_jugar.centerx ,boton_jugar.centery,color.AZUL,40)
    else:
        superficie_transparente = pygame.Surface((boton_jugar.width, boton_jugar.height), pygame.SRCALPHA)
        superficie_transparente.fill((255,255,255,40))
        screen.blit(superficie_transparente,(boton_jugar.x, boton_jugar.y))
        dibujar_texto("Play", boton_jugar.centerx ,boton_jugar.centery,color.BLANCO,40)
    #pygame.draw.rect(screen,(245, 245, 245),boton_jugar)
    if boton_opciones.collidepoint(pygame.mouse.get_pos()):
        sonido_botones()
        pygame.draw.rect(screen,(245, 245, 245),boton_opciones)
        dibujar_texto("Options", boton_opciones.centerx ,boton_opciones.centery,color.AZUL,35)
    else:
        superficie_transparente = pygame.Surface((boton_opciones.width, boton_opciones.height), pygame.SRCALPHA)
        superficie_transparente.fill((255,255,255,40))
        screen.blit(superficie_transparente,(boton_opciones.x, boton_opciones.y))
        dibujar_texto("Options", boton_opciones.centerx ,boton_opciones.centery,color.BLANCO,35)
    if boton_salir.collidepoint(pygame.mouse.get_pos()):
        sonido_botones()
        pygame.draw.rect(screen,(245, 245, 245),boton_salir)
        dibujar_texto("Exit", boton_salir.centerx ,boton_salir.centery,color.AZUL,40)
    else:
        superficie_transparente = pygame.Surface((boton_salir.width, boton_salir.height), pygame.SRCALPHA)
        superficie_transparente.fill((255,255,255,40))
        screen.blit(superficie_transparente,(boton_salir.x, boton_salir.y))
        dibujar_texto("Exit", boton_salir.centerx ,boton_salir.centery,color.BLANCO,40)

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image,(w*scale,h*scale))
    return nueva_imagen



def cargar_animaciones(ruta_carpeta, escala):
    imagenes = []

    for archivo in sorted(os.listdir(ruta_carpeta)):
        if archivo.endswith(".png"):
            ruta_completa = os.path.join(ruta_carpeta,archivo)
            imagen = escalar_img(pygame.image.load(ruta_completa).convert_alpha(), escala)
            imagenes.append(imagen)
    return imagenes


