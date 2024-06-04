import pygame
from game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Scrabble")
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
