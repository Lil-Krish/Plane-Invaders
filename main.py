import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import pygame_menu
import time
import random

pygame.init()

rs = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
bs  = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
gs = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

ys = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

rl = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
bl = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
gl = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))

yl = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

bg = pygame.image.load(os.path.join("assets", "background-black.png"))

width, height = 750, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Jam 1')

running = True

def quit_screen():
    global running
    pygame.quit()
    running = False
    sys.exit()

def play_level_1():
    global running
    while running:
        screen.fill((52, 152, 219))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_screen()

def main():
    global menu_show

    run = True
    FPS = 90
    clock = pygame.time.Clock()

    def reDraw():
        screen.blit(bg, (0,0))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        reDraw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit_screen()

main()
