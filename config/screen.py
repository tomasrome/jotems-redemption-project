import pygame
import src.utils.constantes as constantes

screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

ANCHO_BOTON = 100
ALTO_BOTON = 35

x = (constantes.ANCHO_VENTANA - ANCHO_BOTON) // 2
y = (constantes.ALTO_VENTANA - ALTO_BOTON) // 2

boton_jugar = pygame.Rect(x,y,ANCHO_BOTON,ALTO_BOTON)
boton_controles = pygame.Rect(229,45,15,60)
boton_puntuaciones = pygame.Rect(229,45,15,60)