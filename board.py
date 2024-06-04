import pygame

class Board:
    def __init__(self):
        self.board = [[None for _ in range(15)] for _ in range(15)]

    def draw(self, screen):
        for row in range(15):
            for col in range(15):
                pygame.draw.rect(screen, (255, 255, 255), (col * 40, row * 40, 40, 40), 1)
