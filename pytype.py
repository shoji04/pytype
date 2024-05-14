import pygame
import random

pygame.init()

palavras_teste = [
    "cachorro",
    "gato",
    "macaco",
]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da tela
WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Navinha')

# Carregando imagem da nave
SHIP_WIDTH = 50
SHIP_HEIGHT = 38
ship_img = pygame.image.load('assets/nave.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (SHIP_WIDTH, SHIP_HEIGHT))

# Definindo a classe da nave
class Ship(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Palavra(pygame.sprite.Sprite):
    def __init__(self, palavra):
        pygame.sprite.Sprite.__init__(self)
        self.palavra = palavra
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(self.palavra, True, WHITE)
        self.image = self.text_surface
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speedy = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speedy = random.randint(1, 3)

# Criando a nave
player = Ship(ship_img)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

palavras_sprites = pygame.sprite.Group()
for palavra in palavras_teste:
    p = Palavra(palavra)
    all_sprites.add(p)
    palavras_sprites.add(p)

# Loop principal
game = True
clock = pygame.time.Clock()
FPS = 30

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Atualizando a nave
    all_sprites.update()

    # Desenhando na tela
    background = pygame.image.load('assets/background.png').convert()
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    all_sprites.draw(window)

    pygame.display.update()

pygame.quit()