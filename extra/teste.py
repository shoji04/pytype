import pygame
import random

pygame.init()

lista_facil = ["variavel", "lista", "funçao", "if", "else", "while", "loop", "string", "input", "output"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da tela
WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PyType')

tela_inicial_img = pygame.image.load('assets/tela_inicial.png').convert()
tela_inicial_img = pygame.transform.scale(tela_inicial_img, (WIDTH, HEIGHT))

game_running = False

# Carregando imagem da nave
SHIP_WIDTH = 400
SHIP_HEIGHT = 400
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
for palavra in lista_facil:
    p = Palavra(palavra)
    all_sprites.add(p)
    palavras_sprites.add(p)

# Loop principal
game = True
clock = pygame.time.Clock()
FPS = 30

# Variáveis de jogo
pontuacao = 0
vidas = 3

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # Detecção de entrada do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.speedx = -5
    elif keys[pygame.K_RIGHT]:
        player.speedx = 5
    else:
        player.speedx = 0

    # Atualizando a nave e as palavras
    all_sprites.update()

    # Verificando colisões entre a nave e as palavras
    colisoes = pygame.sprite.spritecollide(player, palavras_sprites, True)
    for colisao in colisoes:
        pontuacao += 100 # Cada palavra destruída concede 100 pontos
        palavra = Palavra(random.choice(lista_facil))
        all_sprites.add(palavra)
        palavras_sprites.add(palavra)

    # Desenhando na tela
    window.fill((0, 0, 0))
    all_sprites.draw(window)

    # Exibindo pontuação e vidas
    font = pygame.font.Font(None, 36)
    texto_pontuacao = font.render(f'Pontuação: {pontuacao}', True, WHITE)
    texto_vidas = font.render(f'Vidas: {vidas}', True, WHITE)
    window.blit(texto_pontuacao, (10, 10))
    window.blit(texto_vidas, (WIDTH - texto_vidas.get_width() - 10, 10))

    pygame.display.update()

pygame.quit()
