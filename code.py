import pygame
import sys
import random

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Dimensiones
ANCHO = 800
ALTO = 600

pygame.init()
time = pygame.time.Clock()

# Configuración
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carreras")

# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

# Clase para los obstáculos
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

    def update(self):
        self.rect.y += 5
        if self.rect.y > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

# Clase para el menú
class Menu:
    def __init__(self, opciones):
        self.opciones = opciones
        self.font = pygame.font.Font(None, 36)
        self.seleccion = 0

    def dibujar(self, ventana):
        for i, opcion in enumerate(self.opciones):
            texto = self.font.render(opcion, 1, WHITE)
            pos = (ANCHO // 2 - texto.get_width() // 2, 200 + i * 50)
            ventana.blit(texto, pos)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.seleccion = (self.seleccion - 1) % len(self.opciones)
                elif event.key == pygame.K_DOWN:
                    self.seleccion = (self.seleccion + 1) % len(self.opciones)
                elif event.key == pygame.K_RETURN:
                    return self.seleccion
        return None

# Menús
menu_inicio = Menu(["Jugar", "Salir"])
menu_final = Menu(["Reiniciar", "Salir"])

# Juego
def juego():
    all_sprites = pygame.sprite.Group()
    obstaculos = pygame.sprite.Group()
    jugador = Jugador()
    all_sprites.add(jugador)

    for i in range(5):
        obstaculo = Obstaculo()
        all_sprites.add(obstaculo)
        obstaculos.add(obstaculo)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        all_sprites.update()

        # Comprobar colisiones
        hits = pygame.sprite.spritecollide(jugador, obstaculos, False)
        if hits:
            game_over = True

        # Dibujar
        ventana.fill((0, 0, 0))
        all_sprites.draw(ventana)
        pygame.display.flip()
        time.tick(30)

    return menu_final

# Loop principal
menu_actual = menu_inicio

while True:
    seleccion = menu_actual.manejar_eventos()

    if seleccion == 0:
        menu_actual = juego()
    elif seleccion == 1:
        break

    ventana.fill((0, 0, 0))
    menu_actual.dibujar(ventana)
    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
