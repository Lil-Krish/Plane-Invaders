import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Name_of_Game')

running = True

def quit_screen():
    global running
    pygame.quit()
    running = False
    sys.exit()

while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_screen()
