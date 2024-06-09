import pygame
from tile import Tile

COLORS = {
    'L2': (139, 200, 234),
    'L3': (34, 134, 189),
    'S2': (255, 192, 203),
    'S3': (192, 89, 77),
    'S4': (226, 21, 21),
    'default': (197, 197, 210),
}


class Board:
    def __init__(self):
        self.grid = self.create_board()
        self.score_font = pygame.font.Font(None, 32)

    def create_board(self):
        special_tiles = {
            (0, 0): 'S4', (0, 3): 'L2', (0, 7): 'S3', (0, 11): 'L2', (0, 14): 'S4',
            (1, 1): 'S2', (1, 5): 'L3', (1, 9): 'L3', (1, 13): 'S2',
            (2, 2): 'S2', (2, 6): 'L2', (2, 8): 'L2', (2, 12): 'S2',
            (3, 0): 'L2', (3, 3): 'S2', (3, 7): 'L2', (3, 11): 'S2', (3, 14): 'L2',
            (4, 4): 'S2', (4, 10): 'S2',
            (5, 1): 'L3', (5, 5): 'L3', (5, 9): 'L3', (5, 13): 'L3',
            (6, 2): 'L2', (6, 6): 'L2', (6, 8): 'L2', (6, 12): 'L2',
            (7, 0): 'S3', (7, 3): 'L2', (7, 7): 'S2', (7, 11): 'L2', (7, 14): 'S3',
            (8, 2): 'L2', (8, 6): 'L2', (8, 8): 'L2', (8, 12): 'L2',
            (9, 1): 'L3', (9, 5): 'L3', (9, 9): 'L3', (9, 13): 'L3',
            (10, 4): 'S2', (10, 10): 'S2',
            (11, 0): 'L2', (11, 3): 'S2', (11, 7): 'L2', (11, 11): 'S2', (11, 14): 'L2',
            (12, 2): 'S2', (12, 6): 'L2', (12, 8): 'L2', (12, 12): 'S2',
            (13, 1): 'S2', (13, 5): 'L3', (13, 9): 'L3', (13, 13): 'S2',
            (14, 0): 'S4', (14, 3): 'L2', (14, 7): 'S3', (14, 11): 'L2', (14, 14): 'S4'
        }

        grid = []
        for y in range(15):
            row = []
            for x in range(15):
                if (y, x) in special_tiles:
                    modifier = special_tiles[(y, x)]
                    color = COLORS[modifier]
                    row.append(Tile(modifier=modifier, color=color))
                else:
                    row.append(Tile())
            grid.append(row)

        return grid

    def draw(self, screen):
        for y in range(15):
            for x in range(15):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                self.grid[y][x].rect.topleft = rect.topleft
                self.grid[y][x].draw(screen, rect.topleft)

    def place_tile(self, x, y, tile):
        self.grid[y][x] = tile

    def draw_player_score(self, screen, player_score):
        x_start = 610  # Prawa strona planszy, szerokość tablicy to 600, więc zaczynamy od 610

        # Rysowanie prostokąta dla wyników
        pygame.draw.rect(screen, (205, 133, 63), [x_start, 0, 180, 600])

        # Rysowanie tytułu "Your Points"
        score_title = self.score_font.render("Your Points", True, (0, 0, 0))
        screen.blit(score_title, (x_start + 20, 20)) # jedna powierzchnia jest kopiowana na druga

        # Miejsce na wyniki gracza (później można tu dodawać wyniki)
        # Rysowanie całkowitego wyniku na dole prostokąta
        total_score = self.score_font.render(f"Total Score: {player_score}", True, (0, 0, 0))
        screen.blit(total_score, (x_start + 20, 560))




