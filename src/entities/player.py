
from src.utils.funciones import cargar_animaciones
from assets.sounds.sounds import sonido_jump, sonido_land, sonido_run, sonido_attack
import pygame

class Player():
    def __init__(self, x, y):
        self.animaciones = {
            "idle" : cargar_animaciones("assets/image/characters/player/idle", 3),
            "run" : cargar_animaciones("assets/image/characters/player/run", 3),
            "jump" : cargar_animaciones("assets/image/characters/player/jump", 3),
            "fall" : cargar_animaciones("assets/image/characters/player/fall", 3),
            "attack" : cargar_animaciones("assets/image/characters/player/attack", 3),
        }
        self.cooldowns = {
            "idle": 120,
            "run": 75,
            "jump": 75,
            "fall": 75,
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
        self.gravedad = 2
        self.fuerza_salto = -28
        self.en_el_suelo = True
        self.atacando = False

        self.flip = False
        self.ultimo_paso = 0
    
    def updates(self):

        #Salto
        self.vel_y += self.gravedad
        self.pos_y += self.vel_y

        if self.pos_y >= 631:
            self.pos_y = 631
            self.vel_y = 0
            self.en_el_suelo = True
        
        if self.en_el_suelo and self.estado_anterior == "fall":
            sonido_land()
        
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

        if self.estado == "run" and self.frame_index in [0, 3, 7, 9]:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_paso > 120: 
                sonido_run()
                self.ultimo_paso = ahora


    def dibujar(self, superficie):
        imagem_flip = pygame.transform.flip(self.image, self.flip, False)
        superficie.blit(imagem_flip, self.forma)
        pygame.draw.rect(superficie, (0, 255, 0), self.forma, 2)
        hitbox = self.get_hitbox()
        if hitbox:
            pygame.draw.rect(superficie, (255, 0, 0), hitbox, 2)
    

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
            sonido_jump()
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
            sonido_attack()
    
    def get_hitbox(self):
        if not self.atacando:
            return None
        
        if self.estado == "attack" and self.frame_index in [4, 5, 6]:  
            if self.flip:
                return pygame.Rect(self.forma.left, self.forma.top + 20, 200, self.forma.height // 2)
            else:
                return pygame.Rect(self.forma.right - 200, self.forma.top + 20, 200, self.forma.height // 2)
        
        return None