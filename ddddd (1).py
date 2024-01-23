import random
import sys

import pygame
import pygame.freetype

pygame.init()
screen = pygame.display.set_mode((900, 500))
pygame.display.set_caption('динозаврик')
clock = pygame.time.Clock()
font = pygame.freetype.Font(None, 40)
cactus_image = pygame.image.load('cactus.png')
cactus_image = pygame.transform.scale(cactus_image, (50, 80))
dino_image = pygame.image.load('dino.png')
dino_image = pygame.transform.scale(dino_image, (100, 100))
ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image, (800, 142))

ground_group = pygame.sprite.Group()
cactus_group = pygame.sprite.Group()

ground_event = pygame.USEREVENT
cactus_event = pygame.USEREVENT + 1
pygame.time.set_timer(ground_event, 2000)
pygame.time.set_timer(cactus_event, 6000)
a = random.randint(30, 99)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Игра в динозаврика", "",
                  "Игра была написанна в трезвом состоянии",
                  "НАДЕЮСЬ ВАМ ПОНРАВИТСЯ"]

    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(60)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Ground(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()
            if a < 60:
                dino.score += 1
            elif a >= 60 and a < 90:
                dino.score += 2
            else:
                dino.score += 3
        if self.rect.colliderect(dino.rect):
            dino.game_status = 'Menu'


class Dino():
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.y = 0
        self.step = 5
        self.max_jump = 90
        self.in_jump = False
        self.score = 0
        self.game_status = 'Game'

    def jump(self):
        if self.in_jump:
            if self.y < self.max_jump:
                self.y += 2
                self.rect.y -= self.step
            elif self.y < self.max_jump * 2:
                self.y += 2
                self.rect.y += self.step
            else:
                self.in_jump = False
                self.y = False

    def draw(self):
        screen.blit(self.image, self.rect)


start_screen()
dino = Dino(dino_image, (80, 400))
g = Ground(ground_image, (300, 450))
ground_group.add(g)
g = Ground(ground_image, (900, 450))
ground_group.add(g)


def game_loop():
    global g
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                dino.in_jump = True
                if dino.game_status == 'Menu':
                    dino.game_status = 'Game'
                    for x in cactus_group:
                        x.kill()
                    dino.score = 0
            if event.type == ground_event:
                g = Ground(ground_image, (900, 450))
                ground_group.add(g)
            if event.type == cactus_event:
                pygame.time.set_timer(cactus_event, random.randint(6000, 10000))
                c = Cactus(cactus_image, (910, 420))
                cactus_group.add(c)

        screen.fill((255, 255, 255))
        if dino.game_status == 'Game':
            ground_group.update()
            ground_group.draw(screen)
            cactus_group.update()
            cactus_group.draw(screen)
            dino.jump()
            dino.draw()
            font.render_to(screen, (850, 50), str(dino.score), (0, 0, 0))
        else:
            font.render_to(screen, (350, 200), 'Game over', (0, 0, 0))
        pygame.display.flip()
        clock.tick(a)


game_loop()

