import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import pygame_menu
import time
import random

pygame.font.init()

pygame.init()

width, height = 750, 750

rs = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
bs  = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
gs = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

ys = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

rl = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
bl = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
gl = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))

yl = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (width, height))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Jam 1')

running = True

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Good(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = ys
        self.laser_img = yl
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Bad(Ship):
    cm = {
            "red": (rs, rl),
            "blue": (bs, bl),
            "green": (gs, gl),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.cm[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, spe):
        self.y += spe

def quit_screen():
    global running
    pygame.quit()
    running = False
    sys.exit()

def main():
    global menu_show

    run = True
    FPS = 90
    level = 0
    lives = 5
    mf = pygame.font.SysFont('comicsans', 50)
    lf = pygame.font.SysFont('comicsans', 60)

    enemies = []
    wl = 5
    esp = 1

    sp = 5
    ply = Good(300, 650)

    clock = pygame.time.Clock()

    l = False
    lc = 0

    def reDraw():
        screen.blit(bg, (0,0))
        livl = mf.render(f'Lives: {lives}', 1, (52, 152, 219))
        levl = mf.render(f'Level: {level}', 1, (52, 152, 219))

        screen.blit(livl, (10, 10))
        screen.blit(levl, (width - levl.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        ply.draw(screen)

        if l:
            ll = lf.render("You Lost.", 1, (52, 152, 219))
            screen.blit(ll, (width / 2 - ll.get_width() / 2, height / 2 - ll.get_height() / 2))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        reDraw()

        if (lives <= 0) or (ply.health <= 0):
            l = True
            lc += 1

        if l:
            if lc > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wl += 5
            for i in range(wl):
                enemy = Bad(random.randrange(50, width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_screen()

        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_LEFT]) or (keys[pygame.K_a])) and (ply.x - sp > 0):
            ply.x -= sp
        if ((keys[pygame.K_RIGHT]) or (keys[pygame.K_d])) and (ply.x + sp + ply.get_width() < width):
            ply.x += sp
        if ((keys[pygame.K_DOWN]) or (keys[pygame.K_s])) and (ply.y + sp + ply.get_height() < height):
            ply.y += sp
        if ((keys[pygame.K_UP]) or (keys[pygame.K_w])) and (ply.y - sp > 0):
            ply.y -= sp

        for enemy in enemies[:]:
            enemy.move(esp)
            if enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)


main()
