import pygame
from src.utils.funciones import cargar_animaciones
from assets.color.color import BLANCO, ROJO, VERDE

class Skeleton():
    def __init__(self, x, y):
        self.animaciones = {
            "idle": cargar_animaciones("assets/image/characters/enemies/skeleton/idle", 2.4),
            "walk": cargar_animaciones("assets/image/characters/enemies/skeleton/walk", 2.4),
            "attack": cargar_animaciones("assets/image/characters/enemies/skeleton/attack", 2.4),
            "hit": cargar_animaciones("assets/image/characters/enemies/skeleton/hit", 2.4),
            "dead": cargar_animaciones("assets/image/characters/enemies/skeleton/dead", 2.4)
        }
        self.estado = "idle"
        self.estado_anterior = self.estado
        self.cooldowns = {
            "idle": 200,
            "walk": 100,
            "attack": 50,
            "hit": 30,
            "dead": 80
        }
        
        self.atacando = False
        self.fue_golpeado = False
        self.reproduciendo_hit = False
        self.invulnerable = False  
        self.tiempo_invulnerabilidad = 500  
        self.ultimo_golpe = 0
        self.muriendo = False  
        self.muerto_completamente = False  
        
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (x, y)

        self.pos_x = x
        self.pos_y = y
        
        self.posicion_absoluta_x = x
        self.posicion_absoluta_y = y
        
        self.posicion_actual = x

        self.flip = False
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vida = 100
        self.vida_max = 100
        self.vivo = True
        self.danio_base = 25  


    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        cooldown = self.cooldowns.get(self.estado, 120)

        if self.invulnerable and tiempo_actual - self.ultimo_golpe > self.tiempo_invulnerabilidad:
            self.invulnerable = False

        if self.fue_golpeado and not self.reproduciendo_hit and not self.invulnerable and self.vivo:
            self.recibir_daño()

        if self.estado != self.estado_anterior:
            self.frame_index = 0
            self.update_time = tiempo_actual
            self.estado_anterior = self.estado

        if tiempo_actual - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = tiempo_actual
        
        if self.frame_index >= len(self.animaciones[self.estado]):
            if self.estado == "dead":
                self.frame_index = len(self.animaciones[self.estado]) - 1
                self.muerto_completamente = True
            else:
                self.frame_index = 0
                if self.estado == "attack":
                    self.atacando = False
                    self.estado = "idle"
                elif self.estado == "hit":
                    if self.vida <= 0:
                        self.estado = "dead"
                        self.muriendo = True
                        self.frame_index = 0
                        self.update_time = tiempo_actual
                    else:
                        self.estado = "idle"
                    self.reproduciendo_hit = False

        self.image = self.animaciones[self.estado][self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.midbottom = (self.pos_x, self.pos_y)
        self.rect = self.forma  


    def recibir_daño(self, daño=None):
        if daño is None:
            daño = self.danio_base
            
        self.vida -= daño
        
        if self.atacando:
            self.atacando = False
        
        self.estado = "hit"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.fue_golpeado = False
        self.reproduciendo_hit = True
        self.invulnerable = True
        self.ultimo_golpe = pygame.time.get_ticks()    

        if self.vida <= 0:
            self.vida = 0
            self.vivo = False


    def movimiento(self, delta_x):
        if self.reproduciendo_hit or not self.vivo or self.atacando:
            return
            
        if delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False
        
        self.pos_x += delta_x
        self.posicion_absoluta_x += delta_x


    def actualizar_posicion_pantalla(self, nueva_pos_x):
        self.pos_x = nueva_pos_x
        self.forma.midbottom = (self.pos_x, self.pos_y)

    def establecer_posicion_absoluta(self, pos_absoluta_x):
        self.posicion_absoluta_x = pos_absoluta_x

    def obtener_posicion_absoluta(self):
        return self.posicion_absoluta_x

    def controlar_estado(self, teclas):
        if not self.vivo or self.muriendo:
            return
            
        if self.reproduciendo_hit:
            return
            
        if self.atacando:
            return
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]:
            self.estado = "walk"
        else:
            self.estado = "idle"
    
    def dibujar(self, superficie):
        if self.invulnerable and not self.muriendo and self.vivo:
            tiempo_transcurrido = pygame.time.get_ticks() - self.ultimo_golpe
            if (tiempo_transcurrido // 100) % 2 == 0:  
                return  
        
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        superficie.blit(imagen_flip, self.forma)
        
        if self.vivo:
            self.dibujar_barra_vida(superficie)
        
        #pygame.draw.rect(superficie, (255, 0, 0), self.forma, 2)

    def dibujar_barra_vida(self, superficie):
        if not self.vivo:
            return
            
        barra_ancho = 60
        barra_alto = 8
        
        if self.estado == "attack":
            barra_x = self.forma.centerx - barra_ancho // 2
            barra_y = self.forma.top + 70
        else:
            barra_x = self.forma.centerx - barra_ancho // 2
            barra_y = self.forma.top - 15
        
        #pygame.draw.rect(superficie, VERDE, (barra_x, barra_y, barra_ancho, barra_alto))
        
        vida_porcentaje = self.vida / self.vida_max
        vida_ancho = int(barra_ancho * vida_porcentaje)
        if vida_ancho > 0:
            pygame.draw.rect(superficie, ROJO, (barra_x, barra_y, vida_ancho, barra_alto))
        
        pygame.draw.rect(superficie, BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 1)

    def atacar(self):
        if not self.atacando and self.vivo and not self.reproduciendo_hit:
            self.estado = "attack"
            self.atacando = True
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def recibir_golpe(self, daño=None):
        if self.vivo and not self.invulnerable:
            self.fue_golpeado = True
            if daño is not None:
                self.danio_base = daño

    def esta_vivo(self):
        return self.vivo
    
    def esta_completamente_muerto(self):
        return self.muerto_completamente
    
    def get_vida_porcentaje(self):
        return self.vida / self.vida_max if self.vida_max > 0 else 0