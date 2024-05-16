import pygame
import random
import sys

pygame.init()

lista_facil = ["variavel", "lista", "funçao", "if", "else", "while", "loop", "string", "input", "output"]

lista_medio = ["recursao", "dicionario", "classe", "metodo", "biblioteca", "exceção", "iterador", "indexaçao", "argumento", "condicional"]

lista_dificil = ["polimorfismo", "herança", "encapsulamento", "compreensão", "modulo", "programaçao", "algoritmo", "arquivos", "exceçoes"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pontuacao = 0

# Configurações da tela
WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PyType')

tela_inicial_img = pygame.image.load('assets/tela_inicial.png').convert()
tela_inicial_img = pygame.transform.scale(tela_inicial_img, (WIDTH, HEIGHT))

gameover_img = pygame.image.load('assets/gameover.png').convert()
gameover_img = pygame.transform.scale(gameover_img, (300, 80))

game_running = False

# Loop principal
clock = pygame.time.Clock()
FPS = 30

while not game_running:
    window.blit(tela_inicial_img, (0, 0))  # Desenha a tela inicial
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game_running = True

# Carregando imagem da nave
SHIP_WIDTH = 60
SHIP_HEIGHT = 60
ship_img = pygame.image.load('assets/nave.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (SHIP_WIDTH, SHIP_HEIGHT))

# Carregando imagem do tiro
SHOT_WIDTH = 16
SHOT_HEIGHT = 50
shot_img = pygame.image.load('assets/tiro.png').convert_alpha()
shot_img = pygame.transform.scale(shot_img, (SHOT_WIDTH, SHOT_HEIGHT))

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

# Definindo a classe do tiro
class Shot(pygame.sprite.Sprite):
    def __init__(self, img, ship_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top

    def update(self):
        self.rect.y -= 8  # Velocidade do tiro

# Criando a nave
player = Ship(ship_img)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

palavras_sprites = pygame.sprite.Group()
for palavra in lista_facil:
    p = Palavra(palavra)
    all_sprites.add(p)
    palavras_sprites.add(p)

shots = pygame.sprite.Group()  # Grupo para os tiros

# Loop principal
game = True
clock = pygame.time.Clock()
FPS = 30

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Dispara o tiro quando a tecla de espaço é pressionada
                shot = Shot(shot_img, player.rect)
                all_sprites.add(shot)
                shots.add(shot)

    # Atualizando a nave e os tiros
    all_sprites.update()
    shots.update()

    for palavra_sprite in palavras_sprites:
        if palavra_sprite.rect.bottom >= HEIGHT:
            window.blit(gameover_img, (WIDTH // 2 - 150, HEIGHT // 2 - 40))
            pygame.display.update()
            pygame.time.delay(2000)  # Aguarda 2 segundos antes de sair do jogo
            pygame.quit()
            sys.exit()

    # Desenhando na tela
    background = pygame.image.load('assets/back.png').convert()
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    all_sprites.draw(window)
    
    def render_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        window.blit(text_surface, text_rect)
    
    render_text("Pontuação: {}".format(pontuacao), pygame.font.Font(None, 40), WHITE, 20, 20)

    pygame.display.update()

pygame.quit()
