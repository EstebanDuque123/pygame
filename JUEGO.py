import pygame
import sys
from pygame.locals import *
from random import randint

# Variables Globales
ancho = 900
alto = 480
ListaEnemigo = []
puntuacion_inicial = 1000  # Puntuación inicial

class naveEspacial(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load("Img/nave.png")
        self.rect = self.ImagenNave.get_rect()
        self.rect.centerx = ancho / 2
        self.rect.centery = alto - 30
        self.listaDisparo = []
        self.Vida = True
        self.velocidad = 20
        self.sonidoDisparo = pygame.mixer.Sound("Sound/Disparo.mp3")
        self.sonidoExplosion = pygame.mixer.Sound("Sound/Explosion.mp3")  # Cargar el sonido de explosión
    
    def movimiento(self):
        if self.Vida:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > ancho - 30:
                self.rect.right = ancho - 30
    
    def disparar(self, x, y):
        miProyectil = Proyectil(x, y, "Img/disparo.png", True)
        self.listaDisparo.append(miProyectil)
        self.sonidoDisparo.play()
    
    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect)

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, posx, posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)
        self.imageProyectil = pygame.image.load(ruta)
        self.rect = self.imageProyectil.get_rect()
        self.velocidadDisparo = 10
        self.rect.top = posy
        self.rect.left = posx
        self.disparoPersonaje = personaje
    
    def trayectoria(self):
        if self.disparoPersonaje:
            self.rect.top -= self.velocidadDisparo
        else:
            self.rect.top += self.velocidadDisparo
    
    def dibujar(self, superficie):
        superficie.blit(self.imageProyectil, self.rect)

class Invasor(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagenEnemigo = pygame.image.load("Img/enemigo.png")
        self.rect = self.imagenEnemigo.get_rect()
        self.listaDisparo = []
        self.velocidad = 5
        self.rect.top = posy
        self.rect.left = posx
        self.tiempoCambio = 1
        self.rangoDisparo = 2  # Aumenta el rango para hacer los disparos más frecuentes
        self.derecha = True
        self.contador = 0
        self.Maxdescenso = self.rect.top + 40
        self.sonidoDisparoE = pygame.mixer.Sound("Sound/DisparoE.mp3")
    
    def dibujar(self, superficie):
        superficie.blit(self.imagenEnemigo, self.rect)
    
    def comportamiento(self):
        self.__ataque()
        self.__movimientos()
    
    def __movimientos(self):
        if self.contador < 3:
            self.__movimientoLateral()
        else:
            self.__descenso()
    
    def __descenso(self):
        if self.Maxdescenso <= self.rect.top:
            self.contador = 0
            self.Maxdescenso = self.rect.top + 40
        else:
            self.rect.top += 1
    
    def __movimientoLateral(self):
        if self.derecha:
            self.rect.left += self.velocidad
            if self.rect.left > ancho - 50:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left -= self.velocidad
            if self.rect.left < 0:
                self.derecha = True
    
    def __ataque(self):
        if randint(0, 100) < self.rangoDisparo:
            self.__disparo()
    
    def __disparo(self):
        x, y = self.rect.center
        miProyectil = Proyectil(x, y, "Img/disparoe.png", False)
        self.listaDisparo.append(miProyectil)
        self.sonidoDisparoE.play()

def cargarEnemigos():
    enemigo = Invasor(100, 100)
    ListaEnemigo.append(enemigo)

def mostrar_texto(ventana, texto, tamano, color, posicion):
    fuente = pygame.font.SysFont("Arial", tamano)
    mensaje = fuente.render(texto, True, color)
    ventana.blit(mensaje, posicion)

def manejar_fin_de_juego(ventana, mensaje):
    while True:

        mostrar_texto(ventana, mensaje, 50, (255, 0, 0), (ancho // 2 - 200, alto // 2 - 50))
        mostrar_texto(ventana, "Presiona R para Reiniciar o Q para Salir ?", 30, (255, 255, 255), (ancho // 2 - 200, alto // 2))
        mostrar_texto(ventana, "Juego por JD", 20, (255, 255, 255), (ancho // 2 - 100, alto - 30))

        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_r:  # Tecla R para reiniciar
                    return True
                elif evento.key == K_q:  # Tecla Q para salir
                    pygame.quit()
                    sys.exit()

def DefensoresDeLaTierra():
    pygame.init()
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Defenseores de la Tierra")
    
    ImagenFondo = pygame.image.load("Img/Fondo.jpg")
    ImagenExplosion = pygame.image.load("Img/explosion.png")  # Cargar imagen de explosión
    pygame.mixer.music.load("Sound/Fondo.mp3")
    pygame.mixer.music.play(-1)  # Reproduce en bucle infinito
    jugador = naveEspacial()
    cargarEnemigos()
    
    enJuego = True
    global puntuacion  # Usar la variable global de puntuación
    reloj = pygame.time.Clock()  # Crear un reloj para controlar el tiempo
    
    while True:  # Bucle principal para permitir reinicio
        jugador = naveEspacial()
        ListaEnemigo.clear()
        cargarEnemigos()
        puntuacion = puntuacion_inicial  # Reiniciar la puntuación
        enJuego = True
        reloj = pygame.time.Clock()  # Crear un reloj para controlar el tiempo
        while enJuego:
            tiempo = reloj.tick(60) / 1000.0  # Tiempo transcurrido por fotograma
            if enJuego:
                puntuacion -= len(ListaEnemigo) * tiempo * 10  # Decrecer puntuación por tiempo y número de enemigos
            
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if enJuego:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == K_LEFT:
                            jugador.rect.left -= jugador.velocidad
                        elif evento.key == K_RIGHT:
                            jugador.rect.right += jugador.velocidad
                        elif evento.key == K_SPACE:
                            x, y = jugador.rect.center
                            jugador.disparar(x, y)
            
            ventana.blit(ImagenFondo, (0, 0))
            
            jugador.movimiento()
            
            for enemigo in ListaEnemigo:
                enemigo.comportamiento()
            
            for enemigo in ListaEnemigo:
                enemigo.dibujar(ventana)
            
            jugador.dibujar(ventana)
            
            # Manejar disparos del jugador
            for x in jugador.listaDisparo[:]:
                x.dibujar(ventana)
                x.trayectoria()
                
                if x.rect.top < -10:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in ListaEnemigo[:]:
                        if x.rect.colliderect(enemigo.rect):
                            ventana.blit(ImagenExplosion, enemigo.rect)  # Dibujar la explosión
                            pygame.display.update()
                            jugador.sonidoExplosion.play()  # Reproducir sonido de explosión
                            pygame.time.wait(100)  # Esperar 100 ms para mostrar la explosión
                            ListaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(x)
                            break  # Salir del bucle después de eliminar un enemigo
            
            # Manejar disparos de los enemigos
            for enemigo in ListaEnemigo:
                for x in enemigo.listaDisparo[:]:
                    x.dibujar(ventana)
                    x.trayectoria()
                    
                    if x.rect.top > alto:
                        enemigo.listaDisparo.remove(x)
                    elif x.rect.colliderect(jugador.rect):  # Detectar colisión con el jugador
                        ventana.blit(ImagenExplosion, jugador.rect)  # Dibujar la explosión en el jugador
                        pygame.display.update()
                        jugador.sonidoExplosion.play()  # Reproducir sonido de explosión
                        pygame.time.wait(100)  # Esperar 100 ms para mostrar la explosión
                        jugador.Vida = False
                        enJuego = False  # Terminar el juego
                        puntuacion = 0  # Establecer la puntuación a 0 si el jugador es eliminado
                        break

            # Si no hay enemigos, mostrar mensaje de victoria
            if len(ListaEnemigo) == 0:
                enJuego = False
                mensaje_final = f"¡Ganaste! Puntuación: {int(puntuacion)}"
            elif not jugador.Vida:  # Si el jugador es eliminado, mostrar mensaje de derrota
                mensaje_final = "¡Perdiste! Puntuación: 0"            
            pygame.display.update()
        if manejar_fin_de_juego(ventana, mensaje_final):  # Reiniciar si el jugador presiona 'R'
            
            continue  # Continuar con el bucle principal para reiniciar el juego

DefensoresDeLaTierra()