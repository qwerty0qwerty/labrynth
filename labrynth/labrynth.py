import pygame
from pygame import mixer, sprite, transform, image, display, key, event, time, font, QUIT, K_LEFT, K_RIGHT, K_UP, K_DOWN

pygame.init()
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_p(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_h - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update_e(self):
        if self.rect.x <= 445:
            self.rect.x = 'left'
        if self.rect.x >= 645:
            self.rect.x = 'right'
        if self.rect.x == 'left':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Finish(GameSprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__(player_image, player_x, player_y, 0)
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
class Wall(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

keys = key.get_pressed()

mixer.music.load('jungles.ogg')
mixer.music.play()

FPS = 60
clock = time.Clock()

game_font = font.Font(None, 70)
win_text = game_font.render('¡GANASTE!', True, (0, 255, 0))
lose_text = game_font.render('¡PERDISTE!', True, (255, 0, 0))

win_w = 650
win_h = 450
window = display.set_mode((win_w, win_h))
display.set_caption("Maze Game")
bg = transform.scale(image.load("background.jpg"), (win_w, win_h))
hero = Player('hero.png', 5, win_h - 80, 4)
cyborg = Enemy('cyborg.png', 5, 5, 2)
treasure = Finish('treasure.png', 600, 400)
wall1 = Wall('wall.png', 200, 200)
wall2 = Wall('wall.png', 300, 200)
wall3 = Wall('wall.png', 400, 200)

walls = [wall1, wall2, wall3]

game = True

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    window.blit(bg, (0, 0))
    hero.update_p()
    cyborg.update_e()
    
    for wall in walls:
        wall.reset()
    
    hero.reset()
    cyborg.reset()
    treasure.reset()

    display.update()
    clock.tick(FPS)

    if (sprite.collide_rect(hero, wall1) or 
        sprite.collide_rect(hero, wall2) or 
        sprite.collide_rect(hero, wall3) or 
        sprite.collide_rect(hero, cyborg)):
        window.blit(lose_text, (win_w//2 - 100, win_h//2))
        display.update()
        time.delay(2000)
        game = False
    
    if sprite.collide_rect(hero, treasure):
        window.blit(win_text, (win_w//2 - 100, win_h//2))
        display.update()
        time.delay(2000)
        game = False