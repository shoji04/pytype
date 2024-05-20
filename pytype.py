import pygame
import random
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyType")

# Definindo as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Carregando imagens
ship_img = pygame.image.load('assets/nave.png').convert_alpha()
ship_img = pygame.transform.scale(ship_img, (80, 80))
shot_img = pygame.image.load('assets/tiro.png').convert_alpha()
shot_img = pygame.transform.scale(shot_img, (50, 50))
gameover_img = pygame.image.load('assets/gameover.png').convert_alpha()
gameover_img = pygame.transform.scale(gameover_img, (380, 100))
background = pygame.image.load('assets/back.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
tela_inicial_img = pygame.image.load('assets/tela_inicial.png').convert()
tela_inicial_img = pygame.transform.scale(tela_inicial_img, (WIDTH, HEIGHT))
play_again_img = pygame.image.load('assets/playagain.png').convert_alpha()
play_again_img = pygame.transform.scale(play_again_img, (340, 200))

# Carregando a fonte personalizada para pontuação
score_font_path = 'assets/fontes/Minecraft.ttf'

# Carregando e reproduzindo a música de fundo
pygame.mixer.init()
pygame.mixer.music.load('assets/musica/musica.mp3')
pygame.mixer.music.play(-1)

# Lista de palavras
lista_facil = [
    "variavel", "lista", "funcao", "if", "else", "while", "loop",
    "string", "input", "output", "jogo", "jogador", "nivel",
    "pontos", "tempo", "tela", "cenario", "menu", "botao",
    "score", "vida", "fase", "restart", "move"
]

lista_medio = [
    "recursao", "dicionario", "classe", "metodo", "biblioteca",
    "excecao", "iterador", "indexacao", "argumento", "condicional",
    "evento", "sprite", "colisao", "inimigo", "pontuacao"
]

lista_dificil = [
    "polimorfismo", "heranca", "encapsulamento", "compreensao",
    "modulo", "programacao", "algoritmo", "arquivos", "excecoes",
    "inteligencia", "artificial", "framework", "decorador", "otimizacao"
]

# Pontuação
pontuacao = 0
word_speed = 1  # Inicializa a velocidade da palavra

class Ship(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

class Palavra(pygame.sprite.Sprite):
    def __init__(self, palavra, speed):
        super().__init__()
        self.palavra = palavra
        self.font = pygame.font.Font(None, 50)
        self.image = self.font.render(self.palavra, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speedy = speed
        self.highlighted = False

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

    def render(self, screen):
        color = YELLOW if self.highlighted else WHITE
        self.image = self.font.render(self.palavra, True, color)
        screen.blit(self.image, self.rect.topleft)

class Shot(pygame.sprite.Sprite):
    def __init__(self, img, ship_rect, target):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_rect.centerx
        self.rect.bottom = ship_rect.top
        self.speed = 35
        self.target = target
        self.direction = pygame.Vector2(target.rect.centerx - self.rect.centerx, target.rect.centery - self.rect.centery).normalize()

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        if self.rect.colliderect(self.target.rect):
            self.kill()
            self.target.kill()

def create_sprites():
    global all_sprites, player, palavras_sprites, shots, pontuacao, word_speed
    player = Ship(ship_img)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    palavras_sprites = pygame.sprite.Group()
    palavras_embaralhadas = lista_facil.copy()
    random.shuffle(palavras_embaralhadas)
    for i in range(min(3, len(palavras_embaralhadas))):
        palavra = palavras_embaralhadas[i]
        p = Palavra(palavra, word_speed)
        all_sprites.add(p)
        palavras_sprites.add(p)

    shots = pygame.sprite.Group()

    pontuacao = 0
    word_speed = 1  # Reinicia a velocidade da palavra

def render_text(text, font_size, color, x, y, font_path=None):
    font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    window.blit(text_surface, text_rect)

def show_start_screen():
    window.blit(tela_inicial_img, (0, 0))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen():
    window.blit(gameover_img, (WIDTH // 2 - gameover_img.get_width() // 2, HEIGHT // 2 - 150))
    window.blit(play_again_img, (WIDTH // 2 - play_again_img.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
    show_start_screen()

show_start_screen()

game = True
clock = pygame.time.Clock()
FPS = 60
input_text = ''

create_sprites()

while game:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    all_sprites.update()

    highlighted_palavra = None
    for palavra_sprite in palavras_sprites:
        if input_text == palavra_sprite.palavra:
            input_text = ''
            pontuacao += 100

            if pontuacao >= 3500:
                lista_palavras = lista_facil + lista_medio + lista_dificil
            elif pontuacao >= 2500:
                lista_palavras = lista_facil + lista_medio
            else:
                lista_palavras = lista_facil

            num_palavras = 3
            if pontuacao >= 3000:
                num_palavras = 5
            elif pontuacao >= 2000:
                num_palavras = 4
            elif pontuacao >= 1000:
                num_palavras = 3

            while len(palavras_sprites) < num_palavras:
                nova_palavra = random.choice(lista_palavras)
                p = Palavra(nova_palavra, word_speed)
                all_sprites.add(p)
                palavras_sprites.add(p)

            if pontuacao % 1000 == 0:
                word_speed += 1

            shot = Shot(shot_img, player.rect, palavra_sprite)
            all_sprites.add(shot)
            shots.add(shot)
            break
        elif palavra_sprite.palavra.startswith(input_text):
            highlighted_palavra = palavra_sprite

        if palavra_sprite.rect.bottom >= HEIGHT:
            show_game_over_screen()
            create_sprites()
            input_text = ''
            break

    window.blit(background, (0, 0))
    all_sprites.draw(window)

    render_text(f'{pontuacao}', 40, YELLOW, 20, 20, score_font_path)
    render_text(input_text, 60, YELLOW, WIDTH // 30, HEIGHT - 50)

    pygame.display.flip()

pygame.quit()
sys.exit()
