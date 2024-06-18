import pygame
from tile import Tile, SpecialTile

COLORS = {
    'L2': (139, 200, 234),
    'L3': (34, 134, 189),
    'S2': (255, 192, 203),
    'S3': (192, 89, 77),
    'S4': (226, 21, 21),
    'default': (197, 197, 210),
}

SPECIAL_TILES = {
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


class Board:
    def __init__(self):
        self.grid = self.create_board()
        self.score_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 32)

    def create_board(self):
        grid = []
        for y in range(15):
            row = []
            for x in range(15):
                if (y, x) in SPECIAL_TILES:
                    modifier = SPECIAL_TILES[(y, x)]
                    color = COLORS[modifier]
                    row.append(SpecialTile(modifier=modifier, color=color))
                else:
                    row.append(Tile())
            grid.append(row)

        return grid

    def draw(self, screen):
        for row in range(15):
            for col in range(15):
                rect = pygame.Rect(col * 40, row * 40, 40, 40)
                self.grid[row][col].rect.topleft = rect.topleft
                self.grid[row][col].draw(screen, rect.topleft)

    def place_tile(self, col, row, tile):
        self.grid[row][col] = tile

    def draw_player_score(self, screen, player_score, word_scores):
        x_start = 610  # Prawa strona planszy, szerokość tablicy to 600, więc zaczynamy od 610

        # Rysowanie prostokąta dla wyników
        pygame.draw.rect(screen, (205, 133, 63), [x_start, 0, 230, 600])

        # Rysowanie tytułu 'Your Points'
        score_title = self.score_font.render('Your Points', True, (0, 0, 0))
        screen.blit(score_title, (x_start + 50, 20)) # jedna powierzchnia jest kopiowana na druga

        y_offset = 60  # Początkowy offset dla punktów za słowa
        for word, score in word_scores:
            word_score_text = self.score_font.render(f'{score} : {word} ', True, (0, 0, 0))
            screen.blit(word_score_text, (x_start + 20, y_offset))
            y_offset += 30  # Odstęp pomiędzy kolejnymi wpisami

        # Miejsce na wyniki gracza (później można tu dodawać wyniki)
        # Rysowanie całkowitego wyniku na dole prostokąta
        total_score = self.score_font.render(f'Total Score: {player_score}', True, (0, 0, 0))
        screen.blit(total_score, (x_start + 30, 560))

    def draw_confirm_button(self, screen):
        button_rect = pygame.Rect(670, 615, 140, 40)  # Przesunięcie w górę przycisku 'Zatwierdź'
        pygame.draw.rect(screen, (0, 128, 0), button_rect)  # Zielony kolor przycisku
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)  # Czarny obrys przycisku
        text_surface = self.button_font.render('Zatwierdź', True, (255, 255, 255))  # Biały tekst
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Dodanie przycisku 'Usuń'
        remove_button_rect = pygame.Rect(670, 705, 140, 40)
        pygame.draw.rect(screen, (255, 140, 0), remove_button_rect)  #
        pygame.draw.rect(screen, (0, 0, 0), remove_button_rect, 2)
        remove_text_surface = self.button_font.render('Usuń', True, (255, 255, 255))  # Biały tekst
        remove_text_rect = remove_text_surface.get_rect(center=remove_button_rect.center)
        screen.blit(remove_text_surface, remove_text_rect)

        exchange_button_rect = pygame.Rect(670, 660, 140, 40)
        pygame.draw.rect(screen, (255, 215, 0), exchange_button_rect)
        pygame.draw.rect(screen, (0, 0, 0), exchange_button_rect, 2)
        exchange_text_surface = self.button_font.render('Wymień', True, (255, 255, 255))  # Biały tekst
        exchange_text_rect = exchange_text_surface.get_rect(center=exchange_button_rect.center)
        screen.blit(exchange_text_surface, exchange_text_rect)

        end_game_button_rect = pygame.Rect(670, 750, 140, 40)  # Większy przycisk
        pygame.draw.rect(screen, (255, 0, 0), end_game_button_rect)  # Niebieski kolor przycisku
        pygame.draw.rect(screen, (0, 0, 0), end_game_button_rect, 2)  # Czarny obrys przycisku
        end_game_text_surface = self.button_font.render('Zakończ grę', True, (255, 255, 255))  # Biały tekst
        end_game_text_rect = end_game_text_surface.get_rect(center=end_game_button_rect.center)
        screen.blit(end_game_text_surface, end_game_text_rect)



    def get_tile_at_position(self, position):
        x, y = position
        grid_x = x // 40
        grid_y = y // 40
        if 0 <= grid_x < 15 and 0 <= grid_y < 15:
            return self.grid[grid_y][grid_x]
        return None

    def remove_tile(self, tile):
        for row in range(15):
            for col in range(15):
                if self.grid[row][col] == tile:
                    modifier = None
                    if (row, col) in SPECIAL_TILES:
                        modifier = SPECIAL_TILES[(row, col)]
                    color = COLORS.get(modifier, COLORS['default'])
                    # Tworzymy nowy kafelek na planszy
                    self.grid[row][col] = Tile(modifier=modifier, color=color)
                    return
