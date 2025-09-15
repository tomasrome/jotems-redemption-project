import pygame
""" import src.utils.constantes as constantes """

class Personaje():
    def __init__(self, x, y, animaciones):
        self.animaciones = animaciones
        self.estado = "idle"
        self.estado_anterior = "idle"

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (x, y)

        self.pos_x = x
        self.pos_y = y

        self.flip = False
        self.vel_y = 0
        self.gravedad = 1.2
        self.fuerza_salto = -28
        self.en_el_suelo = True

    def update(self):
        # Actualizar física
        self.vel_y += self.gravedad
        self.pos_y += self.vel_y

        # Límite del suelo
        if self.pos_y >= 365:
            self.pos_y = 365
            self.vel_y = 0
            self.en_el_suelo = True

        # Si el estado cambió, reiniciar animación
        if self.estado != self.estado_anterior:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.estado_anterior = self.estado

        # Animación
        cooldown = 80  # ms por frame
        if pygame.time.get_ticks() - self.update_time >= cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Loop de animación
        if self.frame_index >= len(self.animaciones[self.estado]):
            self.frame_index = 0

        # Actualizar imagen y rect
        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (self.pos_x, self.pos_y)

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        # pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.forma, 1)

    def movimiento(self, delta_x):
        # Movimiento horizontal
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        if self.pos_x + delta_x > 277:
            delta_x = 0
            self.pos_x = 276
        else:
            self.pos_x += delta_x

    def saltar(self):
        if self.en_el_suelo:
            self.vel_y = self.fuerza_salto
            self.en_el_suelo = False
