import pygame
from game import Game
from menu import Menu
from menu import Instructions
from end_game import EndGameScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((850, 800))
    pygame.display.set_caption('Scrabble')

    menu = Menu(screen)
    instructions = Instructions(screen)

    in_menu = True
    show_instructions = False

    while True:  # Główna pętla
        while in_menu or show_instructions:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if in_menu:
                            if menu.check_start_button_click(event.pos):
                                in_menu = False
                            elif menu.check_instructions_button_click(event.pos):
                                show_instructions = True
                                in_menu = False
                        elif show_instructions:
                            if menu.check_start_button_click(event.pos):
                                show_instructions = False
                                in_menu = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and show_instructions:
                        show_instructions = False
                        in_menu = True

            if in_menu:
                menu.draw_menu()
            elif show_instructions:
                instructions.draw_instructions()

        game = Game(screen)
        final_score = game.run()  # Uruchom grę i uzyskaj wynik

        end_screen = EndGameScreen(screen, final_score)
        end_screen.draw()  # Wyświetl ekran końcowy

        # Oczekiwanie na zamknięcie okna ekranu końcowego
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == '__main__':
    main()
