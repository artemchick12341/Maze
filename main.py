import pygame as pg
import pygame_menu
import os
import sys

# Определение базового пути для ресурсов
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

# Функция для загрузки ресурсов
def load_resource(filename):
    return os.path.join(base_path, filename)

pg.init()
try:
    pg.mixer.init()
except pg.error:
    print("Звук недоступен, продолжаем без музыки")

class GameSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(load_resource(filename)), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and self.rect.right < W:
            self.rect.x += self.speed
            if pg.sprite.spritecollide(self, walls, False):
                self.rect.x -= self.speed
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            if pg.sprite.spritecollide(self, walls, False):
                self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            if pg.sprite.spritecollide(self, walls, False):
                self.rect.y += self.speed
        if keys[pg.K_DOWN] and self.rect.bottom < H:
            self.rect.y += self.speed
            if pg.sprite.spritecollide(self, walls, False):
                self.rect.y -= self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update_x(self, x1, x2):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.x <= x1:
            self.direction = 'right'
        if self.rect.right >= x2:
            self.direction = 'left'

    def update_y(self, y1, y2):
        pass

W, H = (700, 500)
FPS = 120
clock = pg.time.Clock()

walls = pg.sprite.Group()
walls.add(
    GameSprite('R_v.png', 20, -42, 20, 600, 0),
    GameSprite('R_v.png', 150, 130, 20, 500, 0),
    GameSprite('R_h.png', 20, -5, 800, 20, 0),
    GameSprite('R_v.png', 250, -5, 20, 200, 0),
    GameSprite('R_v.png', 250, 300, 20, 100, 0),
    GameSprite('R_h.png', 20, -5, 200, 20, 0),
    GameSprite('R_h.png', 150, 480, 800, 20, 0),
    GameSprite('R_h.png', 260, 300, 300, 20, 0),
    GameSprite('R_h.png', 260, 170, 200, 20, 0),
    GameSprite('R_h.png', 260, 378, 290, 20, 0),
    GameSprite('R_v.png', 535, 0, 20, 400, 0),
    GameSprite('R_v.png', 680, 130, 20, 380, 0),
    GameSprite('R_v.png', 437, 7, 20, 170, 0)
)

BACK_IMAGE = pg.transform.scale(pg.image.load(load_resource('background.jpg')), (W, H))
window = pg.display.set_mode((W, H))

def main():
    cyborg = Enemy('cyborg.png', 5, 150, 50, 50, 0.6)
    hero = Player('hero.png', 70, 350, 50, 50, 8)
    pg.mixer.music.load(load_resource('jungles.ogg'))
    pg.mixer.music.play()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if pg.sprite.collide_rect(hero, cyborg):
            end_menu('Вы проиграли(')
        window.blit(BACK_IMAGE, (0, 0))
        cyborg.draw()
        cyborg.update_x(30, 150)
        hero.draw()
        hero.update()
        walls.draw(window)
        if hero.rect.right >= 680 and hero.rect.y > 20 and hero.rect.bottom < 80:
            pg.mixer.music.load(load_resource('money.ogg'))
            pg.mixer.music.play()
            end_menu('Вы выйграли!!!')
            return
        pg.display.update()
        clock.tick(FPS)

def start_menu():
    pg.mixer.music.load(load_resource('jazz.mp3'))
    pg.mixer.music.play()
    menu = pygame_menu.Menu('Лабиринт', 400, 200, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Играть', main)
    menu.add.button('Выйти из игры', pygame_menu.events.EXIT)
    menu.mainloop(window)

def end_menu(text):
    pg.mixer.music.load(load_resource('jazz.mp3'))
    pg.mixer.music.play()
    menu = pygame_menu.Menu('Лабиринт', 400, 200, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.label(text)
    menu.add.button('Сыграть еще раз', main)
    menu.add.button('Выйти в меню', start_menu)
    menu.mainloop(window)

if __name__ == '__main__':
    start_menu()