import pygame
import src.utils.constantes as constantes

screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))

ANCHO_BOTON = 170
ALTO_BOTON = 60

x = (constantes.ANCHO_VENTANA - ANCHO_BOTON) // 2
y = (constantes.ALTO_VENTANA - ALTO_BOTON) // 2

boton_jugar = pygame.Rect(x,y-50,ANCHO_BOTON,ALTO_BOTON)
boton_opciones = pygame.Rect(x,y+50,ANCHO_BOTON,ALTO_BOTON)
boton_salir = pygame.Rect(x,y+150,ANCHO_BOTON,ALTO_BOTON)