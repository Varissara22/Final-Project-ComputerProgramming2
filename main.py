import pygame
import sys

from title_screen import run_title_screen
from maingame     import run_main_game, SCREEN_W, SCREEN_H
from save_system  import load_game, delete_save

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Soul Steep")
    clock  = pygame.time.Clock()

    while True:
        action = run_title_screen(screen, clock)

        if action == 'new_game':
            delete_save()
            run_main_game(screen, clock, save_data=None)

        elif action == 'continue':
            save_data = load_game()
            run_main_game(screen, clock, save_data=save_data)

        elif action == 'exit':
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()