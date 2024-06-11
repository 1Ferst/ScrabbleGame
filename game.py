import pygame
from board import Board
from bag import Bag
from player_rack import PlayerRack
import random

LETTER_VALUES = {
    'A': 1, 'Ą': 5, 'B': 3, 'C': 2, 'Ć': 6, 'D': 2, 'E': 1, 'Ę': 5,
    'F': 5, 'G': 3, 'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2, 'Ł': 3,
    'M': 2, 'N': 1, 'Ń': 7, 'O': 1, 'Ó': 5, 'P': 2, 'R': 1, 'S': 1,
    'Ś': 5, 'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5,
    '_': 0
}


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.bag = Bag()
        self.player_rack = PlayerRack(self.bag)
        self.letter_values = LETTER_VALUES
        self.player_score = 0
        self.player_rack.refill_rack()
        self.dragging_tile = None
        self.dragging_offset_x = 0
        self.dragging_offset_y = 0

        self.current_turn_tiles = []

    def draw_game(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        self.board.draw_player_score(self.screen, self.player_score)
        self.player_rack.draw(self.screen)
        self.board.draw_confirm_button(self.screen)
        if self.dragging_tile:
            self.dragging_tile.draw(self.screen, (pygame.mouse.get_pos()[0] - self.dragging_offset_x, pygame.mouse.get_pos()[1] - self.dragging_offset_y))
        pygame.display.flip()

    def check_button_click(self, pos):
        button_rect = pygame.Rect(650, 660, 120, 40)
        return button_rect.collidepoint(pos)

    def check_remove_button_click(self, pos):
        remove_button_rect = pygame.Rect(650, 750, 120, 40)
        return remove_button_rect.collidepoint(pos)


    def check_exchange_button_click(self, pos):
        remove_button_rect = pygame.Rect(650, 705, 120, 40)
        return remove_button_rect.collidepoint(pos)

    def end_turn(self):
        # Logika zatwierdzania ruchu
        print("Zatwierdzono ruch")
        self.player_rack.refill_rack()
        self.dragging_tile = None
        self.current_turn_tiles = []

    def return_tile_to_rack(self, tile):
        if tile in self.current_turn_tiles:
            self.player_rack.rack.append(tile)
            self.current_turn_tiles.remove(tile)
            self.board.remove_tile(tile)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Lewy przycisk myszy
                        if self.check_button_click(event.pos):
                            self.end_turn()
                        elif self.check_remove_button_click(event.pos):
                            for tile in self.current_turn_tiles[:]:
                                self.player_rack.rack.append(tile)
                                self.current_turn_tiles.remove(tile)
                                self.board.remove_tile(tile)
                        elif self.check_exchange_button_click(event.pos):
                            if self.bag.tiles:  # zobaczenie czy bag nie jest pusty
                                for tile in self.player_rack.rack[:]:
                                    self.bag.tiles.append(tile)
                                    self.player_rack.remove_tile(tile)

                                for tile in self.current_turn_tiles[:]: # w trakcie wymiany, wrzucenie z planszy do worka liter z tury
                                    self.bag.tiles.append(tile)
                                    self.current_turn_tiles.remove(tile)
                                    self.board.remove_tile(tile)
                                random.shuffle(self.bag.tiles)
                                self.player_rack.refill_rack()

                        else:
                            clicked_tile = self.board.get_tile_at_position(event.pos)
                            if clicked_tile:
                                self.return_tile_to_rack(clicked_tile)
                            else:
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
                            if self.board.grid[grid_y][grid_x].letter is None:  # Sprawdzenie, czy pole jest puste
                                self.board.place_tile(grid_x, grid_y, self.dragging_tile)
                                self.current_turn_tiles.append(self.dragging_tile)
                            else:
                                self.player_rack.rack.append(self.dragging_tile)  # Wrzucenie kafelka z powrotem na stojak
                        else:
                            self.player_rack.rack.append(self.dragging_tile)
                            # zmienic na insert zeby przywrocic kafelek na poprzednia pozycja jesli upuscimy poza plansze
                            # lub wcale nie zmieniac pozycji reszty kafelkow do zakonczenia tury
                        self.dragging_tile = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_tile:
                        self.draw_game()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Naciśnięto klawisz Enter
                        self.player_rack.refill_rack()
                        self.current_turn_tiles = []
            # uzupelniac dopiero po zakonczeniu rundy lub w przypadku wymiany liter
            self.draw_game()

        pygame.quit()
