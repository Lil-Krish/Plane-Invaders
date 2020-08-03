import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import pygame_menu
import time
import random
import math

pygame.font.init()

pygame.init()

width, height = 750, 750
times = 0

gp = pygame.image.load(os.path.join("images", "health_power.png"))
rp = pygame.image.load(os.path.join("images", "speed_power.png"))

rs = pygame.transform.scale(pygame.image.load(os.path.join("images", "red_ufo.png")), (70, 50))
bs  = pygame.transform.scale(pygame.image.load(os.path.join("images", "blue_ufo.png")), (50, 30))

gs = pygame.transform.scale(pygame.image.load(os.path.join("images", "green_ufo.png")), (60, 50))

ys = pygame.transform.scale(pygame.image.load(os.path.join("images", "yellow_plane.png")), (70, 70))

rl = pygame.image.load(os.path.join("images", "red_laser.png"))
bl = pygame.image.load(os.path.join("images", "blue_laser.png"))
gl = pygame.image.load(os.path.join("images", "green_laser.png"))

yl = pygame.image.load(os.path.join("images", "yellow_laser.png"))

bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "bg.jpg")), (width, height))

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Jam 1')

class PowerUp:
    global times

    cm = {
            "green": gp,
            "red": rp
    }

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.img = self.cm[color]
        self.mask = pygame.mask.from_surface(self.img)
        self.color = color

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_item(self, obj):
        return collide(self, obj)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, spe):
        self.y += spe

    def offs(self, height):
        return not (self.y <= height and self.y >= 0)

    def coll(self, obj):
        return collide(self, obj)

class Plane:
    cd = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.plane_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown = 0

    def draw(self, window):
        window.blit(self.plane_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def ml(self, spe, obj):
        self.cld()
        for laser in self.lasers:
            laser.move(spe)
            if laser.offs(height):
                self.lasers.remove(laser)
            elif laser.coll(obj):
                obj.health -= 10
                if laser in self.lasers:
                    self.lasers.remove(laser)

    def cld(self):
        if self.cooldown > self.cd:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1

    def shoot(self):
        if self.cooldown == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown = 1

    def get_width(self):
        return self.plane_img.get_width()

    def get_height(self):
        return self.plane_img.get_height()

class Good(Plane):
    global times

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.plane_img = ys
        self.laser_img = yl
        self.mask = pygame.mask.from_surface(self.plane_img)
        self.max_health = health

    def ml(self, spe, objs):
        self.cld()
        for laser in self.lasers:
            laser.move(spe)
            if laser.offs(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.coll(obj):
                        if obj.color == 'red':
                            obj.health -= 50
                            obj.collides_needed -= 1
                            if obj.collides_needed == 0:
                                objs.remove(obj)
                        elif obj.color == 'green':
                            obj.collides_needed -= 1
                            if obj.collides_needed == 0:
                                objs.remove(obj)
                            else:
                                obj.health -= int(((self.max_health) * (1 / (2 ** (times - 2)))))
                        else:
                            objs.remove(obj)

                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.bar(window)

    def bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width() * ((self.health) / (self.max_health)), 10))

    def reset(self):
        self.health = self.max_health

class Bad(Plane):
    cm = {
            "red": (rs, rl),
            "blue": (bs, bl),
            "green": (gs, gl),
    }
    collides_needed = 1

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.color = color
        if color == "red":
            self.collides_needed = 2
            self.max_health = health
        if color == "green":
            self.collides_needed = 1
            self.max_health = health
            self.green_hit = False
            self.speed = 3

        self.plane_img, self.laser_img = self.cm[color]
        self.mask = pygame.mask.from_surface(self.plane_img)

    def move(self, spe):
        if self.color == "green":
            self.y += self.speed
        else:
            self.y += spe

    def shoot(self):
        if self.cooldown == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cooldown = 1

    def draw(self, window):
        super().draw(window)
        self.bar(window)

    def bar(self, window):
        if self.color == 'red':
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width() * ((self.health) / (self.max_health)), 10))
        elif self.color == 'green':
            if (self.green_hit):
                pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width(), 10))
                pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.plane_img.get_height() + 10, self.plane_img.get_width() * ((self.health) / (self.max_health)), 10))
        else:
            pass

    def ml(self, spe, obj):
        self.cld()
        for laser in self.lasers:
            laser.move(spe)
            if laser.offs(height):
                self.lasers.remove(laser)
            elif laser.coll(obj):
                if self.color == "blue":
                    obj.health -= 20
                else:
                    obj.health -= 10

                if laser in self.lasers:
                    self.lasers.remove(laser)

def quit_screen():
    pygame.quit()
    sys.exit()

def collide(obj1, obj2):
    ofs_x = obj2.x - obj1.x
    ofs_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (ofs_x, ofs_y)) != None

index = 0
wait_for_powerup = 0
powerup_show = 0

def main():
    global index, times, green_hit, wait_for_powerup, powerup_show

    run = True
    FPS = 60
    level = 0
    lives = 5
    mf = pygame.font.SysFont('Courier', 50)
    lf = pygame.font.SysFont('Courier', 60)

    enemies = []
    powerups = []

    pl = 5
    wl = 5

    esp = 1
    sp = 5

    lv = 5

    ply = Good(300, 630)

    clock = pygame.time.Clock()

    l = False
    lc = 0

    def reDraw():
        global wait_for_powerup, powerup_show

        screen.blit(bg, (0,0))
        livl = mf.render(f'Lives: {lives}', 1, (52, 152, 219))
        levl = mf.render(f'Level: {level}', 1, (52, 152, 219))

        screen.blit(livl, (10, 10))
        screen.blit(levl, (width - levl.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(screen)

        if not (len(powerups) == 0):
            for i in range(index + 1):
                if wait_for_powerup < FPS * 3:
                    wait_for_powerup += 1
                else:
                    if powerup_show < FPS * 3:
                        powerup_show += 1
                        powerups[i].draw(screen)
                    else:
                        powerups.pop(i)
                        i -= 1


        if (wait_for_powerup >= FPS * 3) and (powerup_show >= FPS * 3):
            wait_for_powerup = 0
            powerup_show = 0

        ply.draw(screen)

        if l:
            ll = lf.render("You Lost.", 1, (0, 0, 0))
            screen.blit(ll, (width / 2 - ll.get_width() / 2, height / 2 - ll.get_height() / 2))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        reDraw()

        if (lives <= 0) or ((ply.health <= 0) and (lives <= 0)):
            l = True
            lc += 1

        if (lives > 0) and (ply.health <= 0):
            lives -= 1
            ply.reset()

        if l:
            if lc > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            wait_for_powerup = 0
            powerup_show = 0

            level += 1
            index = 0
            wl += 5
            pl -= 1

            sp = 5

            for i in range(wl):
                enemy = Bad(random.randrange(50, width - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

            for i in range(pl):
                powerup = PowerUp(random.randrange(50, width - 100), random.randrange(400, width - 100), random.choice(["red", "green"]))
                powerups.append(powerup)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ply.shoot()

        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_LEFT]) or (keys[pygame.K_a])) and (ply.x - sp > 0):
            ply.x -= sp
        if ((keys[pygame.K_RIGHT]) or (keys[pygame.K_d])) and (ply.x + sp + ply.get_width() < width):
            ply.x += sp
        if ((keys[pygame.K_DOWN]) or (keys[pygame.K_s])) and (ply.y + sp + ply.get_height() + 20 < height):
            ply.y += sp
        if ((keys[pygame.K_UP]) or (keys[pygame.K_w])) and (ply.y - sp > 0):
            ply.y -= sp
        if keys[pygame.K_SPACE]:
            ply.shoot()

        def difficulty(diff):
            if round(math.exp(-(diff - 3)), 0) != 0:
                return round(math.exp(-0.25 * (diff - 3)) + 0.5, 0)
            else:
                return 0.05

        for enemy in enemies[:]:
            enemy.move(esp)
            enemy.ml(lv, ply)

            if random.randrange(0, difficulty(level) * 60) == 1:
                enemy.shoot()

            if collide(enemy, ply):
                if enemy.color == "blue":
                    ply.health -= 20
                else:
                    ply.health -= 10

                if enemy.color == 'red' or enemy.color == 'green':
                    enemy.collides_needed -= 1
                    if enemy.collides_needed == 0:
                        enemies.remove(enemy)
                else:
                    enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        for enemy in enemies[:]:
            for pwu in powerups[:]:
                if collide(pwu, enemy):
                    if (enemy.color == "green") and (pwu.color == "green"):
                        enemy.green_hit = True
                        powerups.remove(pwu)
                        enemy.max_health = 2 * enemy.max_health
                        times += 1
                        enemy.health = enemy.max_health
                        enemy.collides_needed = 2 * enemy.collides_needed
                        wait_for_powerup = 0
                        powerup_show = 0
                    elif (enemy.color == "green") and (pwu.color == "red"):
                        powerups.remove(pwu)
                        enemy.speed += 1
                        wait_for_powerup = 0
                        powerup_show = 0
                    else:
                        pass

        for pwu in powerups[:]:
            if collide(pwu, ply):
                powerups.remove(pwu)
                wait_for_powerup = 0
                powerup_show = 0

                if pwu.color == "green":
                    if ply.health + 20 <= ply.max_health:
                        ply.health += 20
                    else:
                        ply.health = ply.max_health
                elif pwu.color == "red":
                    sp += 1

        ply.ml(-lv, enemies)

def menu():
    tf = pygame.font.SysFont('Courier', 70)
    run = True

    while run:
        menu = pygame_menu.Menu(300, 400, 'Welcome', theme=pygame_menu.themes.THEME_BLUE)
        menu.add_text_input('Name: ', default='John Doe')
        menu.add_button('Play', main)
        menu.add_button('Quit', quit_screen)

        menu.mainloop(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                quit_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    quit_screen()

menu()
