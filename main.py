import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((800, 600))
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


menu = pygame_menu.Menu(300, 400, 'Space Invaders', theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Name: ', default='John Doe')
menu.add_button('Play', play_level_1)
menu.add_button('Quit', quit_screen)

menu.mainloop(screen)
