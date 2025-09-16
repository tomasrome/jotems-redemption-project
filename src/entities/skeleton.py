import pygame
from src.utils.funciones import cargar_animaciones

class Skeleton():
    def __init__(self, x,y):
        self.animaciones = {
            "idle" : cargar_animaciones("assets/image/characters/enemies/skeleton/idle",2.4),
            "walk" : cargar_animaciones("assets/image/characters/enemies/skeleton/walk",2.4),
            "attack" : cargar_animaciones("assets/image/characters/enemies/skeleton/attack",2.4),
            "hit" : cargar_animaciones("assets/image/characters/enemies/skeleton/hit",2.4)
        }
        self.estado = "idle"
        self.estado_anterior = self.estado
        self.cooldowns = {
            "idle": 200,
            "walk": 100,
            "attack": 50,
            "hit": 30
        }
        self.atacando = False
        self.atacado = False
        self.fue_golpeado = False
        self.reproduciendo_hit = False
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (x,y)

        self.pos_x = x
        self.pos_y = y

        self.atacando = False

        self.flip = False


    def update(self):

        cooldown = self.cooldowns.get(self.estado,120)

        if self.fue_golpeado and not self.reproduciendo_hit:
            self.estado = "hit"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.fue_golpeado = False
            self.reproduciendo_hit = True

        if self.estado != self.estado_anterior:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.estado_anterior = self.estado

        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animaciones[self.estado]):
            self.frame_index = 0
            if self.estado == "attack":
                self.atacando = False
                self.estado = "idle"
            if self.estado == "hit":
                self.estado = "idle"
                self.reproduciendo_hit = False
        

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (self.pos_x, self.pos_y)

    
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

    def controlar_estado(self, teclas):
        if self.atacando:
            return
        elif self.atacado:
            if not self.ataque_terminado:
                self.estado = "hit"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado = "walk"
        else:
            self.estado = "idle"
    
    def dibujar(self, superficie):
        imagem_flip = pygame.transform.flip(self.image, self.flip, False)
        superficie.blit(imagem_flip, self.forma)
        #pygame.draw.rect(superficie, (255, 0, 0), self.forma, 2)

    def atacar(self):
        if not self.atacando:
            self.estado = "attack"
            self.atacando = True
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def recibir_golpe(self):
        self.fue_golpeado = True
