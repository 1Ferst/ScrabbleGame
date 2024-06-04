import pygame

class Tile:
    def __init__(self, letter, points):
        self.letter = letter
        self.points = points
        self.image = pygame.image.load(f'assets/tiles/{letter}.png')
        self.rect = self.image.get_rect()

    def draw(self, screen, position):
        screen.blit(self.image, position)
