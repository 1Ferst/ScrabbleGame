import pygame
from board import Board
from bag import Bag
from player_rack import PlayerRack

LETTER_VALUES = {
    'A': 1, 'Ą': 5, 'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5,
    'F': 5, 'G': 3, 'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3,
    'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5, 'P': 2, 'R': 1, 'S': 1,
    'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5,
    '_': 0
}


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Scrabble")
        self.board = Board()
        self.bag = Bag()
        self.player_rack = PlayerRack(self.bag)
        self.letter_values = LETTER_VALUES
        self.player_score = 0

        self.dragging_tile = None
        self.dragging_offset_x = 0
        self.dragging_offset_y = 0

    def draw_game(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        self.board.draw_player_score(self.screen, self.player_score)
        self.player_rack.draw(self.screen)
        if self.dragging_tile:
            self.dragging_tile.draw(self.screen, (pygame.mouse.get_pos()[0] - self.dragging_offset_x, pygame.mouse.get_pos()[1] - self.dragging_offset_y))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Lewy przycisk myszy
                        clicked_tile = self.player_rack.get_tile_at_position(event.pos)
                        if clicked_tile:
                            self.dragging_tile = clicked_tile
                            self.dragging_offset_x = event.pos[0] - clicked_tile.rect.x
                            self.dragging_offset_y = event.pos[1] - clicked_tile.rect.y
                            self.player_rack.remove_tile(clicked_tile)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging_tile:  # Lewy przycisk myszy
                        grid_x = event.pos[0] // 40
                        grid_y = event.pos[1] // 40
                        if 0 <= grid_x < 15 and 0 <= grid_y < 15:
                            self.board.place_tile(grid_x, grid_y, self.dragging_tile)
                        else:
                            self.player_rack.rack.append(self.dragging_tile) #
                            # zmienic na insert zeby przywrocic kafelek na poprzednia pozycja jesli upuscimy poza plansze
                            # lub wcale nie zmieniac pozycji reszty kafelkow do zakonczenia tury
                        self.dragging_tile = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_tile:
                        self.draw_game()

            self.player_rack.refill_rack()
            # uzupelniac dopiero po zakonczeniu rundy lub w przypadku wymiany liter
            self.draw_game()

        pygame.quit()
