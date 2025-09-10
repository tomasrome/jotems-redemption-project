
from funciones import cargar_animaciones
import pygame

class Player():
    def __init__(self, x, y):
        self.animaciones = {
            "idle" : cargar_animaciones("assets/image/characters/player/idle", 2.2),
            "run" : cargar_animaciones("assets/image/characters/player/run", 2.2),
            "jump" : cargar_animaciones("assets/image/characters/player/jump", 2.2),
            "fall" : cargar_animaciones("assets/image/characters/player/fall", 2.2),
            "attack" : cargar_animaciones("assets/image/characters/player/attack", 2.2),
        }
        self.cooldowns = {
            "idle": 175,
            "run": 100,
            "jump": 100,
            "fall": 100,
            "attack": 50,

        }
        self.estado = "idle"
        self.estado_anterior = "idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (x,y)

        self.pos_x = x
        self.pos_y = y

        self.vel_y = 0
        self.gravedad = 1.2
        self.fuerza_salto = -18
        self.en_el_suelo = True
        self.atacando = False

        self.flip = False
    
    def updates(self):

        #Salto
        self.vel_y += self.gravedad
        self.pos_y += self.vel_y

        if self.pos_y >= 365:
            self.pos_y = 365
            self.vel_y = 0
            self.en_el_suelo = True
        
        if self.estado != self.estado_anterior:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.estado_anterior = self.estado
        
        
        cooldown = self.cooldowns.get(self.estado)

        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animaciones[self.estado]):
            self.frame_index = 0
            if self.estado == "attack":
                self.atacando = False
                self.estado = "idle"
        
        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (self.pos_x, self.pos_y)


    def dibujar(self, superficie):
        imagem_flip = pygame.transform.flip(self.image, self.flip, False)
        superficie.blit(imagem_flip, self.forma)
        #pygame.draw.rect(superficie, (0, 255, 0), self.forma, 2)
    

    def movimiento(self, delta_x):
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False
        
        #if self.pos_x + delta_x > 277:
           # delta_x = 0
            #self.pos_x = 276
        #else:
        self.pos_x += delta_x
        
    

    def saltar(self):
        if self.en_el_suelo:
            self.vel_y = self.fuerza_salto
            self.en_el_suelo = False

    def controlar_estado(self, teclas):
        if self.atacando:
            return

        if not self.en_el_suelo:
            if self.vel_y <= 2:
                self.estado = "jump"
            else:
                self.estado = "fall"
        elif teclas[pygame.K_a] or teclas[pygame.K_d]:
            self.estado = "run"
        else:
            self.estado = "idle"

    def atacar(self):
        if not self.atacando:
            self.estado = "attack"
            self.atacando = True
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    