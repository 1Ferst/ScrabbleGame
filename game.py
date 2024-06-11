import pygame
from board import Board
from bag import Bag
from player_rack import PlayerRack
import random
import word_checker

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

        self.words_on_board = set()
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

    def get_neighbors_horizontally(self, row, col):
        neighbors = set()
        if row > 0:
            neighbors.add(self.board.grid[row - 1][col])
        if row < 14:
            neighbors.add(self.board.grid[row + 1][col])

        return neighbors

    def get_neighbors_vertically(self, row, col):
        neighbors = set()
        if col > 0:
            neighbors.add(self.board.grid[row][col - 1])
        if col < 14:
            neighbors.add(self.board.grid[row][col + 1])

        return neighbors

    def is_constant_straight_line_with_neighbor(self, tiles):
        if not tiles:
            return False

        rows = [tile[1] for tile in tiles]  # y
        cols = [tile[0] for tile in tiles]  # x

        # EDIT potrzebne wyswietlanie info dla uzytkownika
        if self.words_on_board and (7, 7) not in [(tile[0], tile[1]) for tile in tiles]:
            print('Pierwsze słowo musi być na środku')
            return False
        # Sprawdzenie czy wszystkie kafelki są w jednej linii
        is_straight = len(set(rows)) == 1 or len(set(cols)) == 1
        if not is_straight:
            return False

        # Sprawdzenie ciągłości
        if len(set(rows)) == 1:  # Wszystkie kafelki w jednym wierszu
            row = rows[0]
            min_col, max_col = min(cols), max(cols)
            for col in range(min_col, max_col + 1):
                if self.board.grid[row][col].letter is None:
                    return False
                # Sprawdzenie sąsiadów
                if self.words_on_board:
                    neighbors = self.get_neighbors_vertically(row, col)
                    if not any(neighbor.letter is not None for neighbor in neighbors):
                        return False

        else:  # Wszystkie kafelki w jednej kolumnie
            col = cols[0]
            min_row, max_row = min(rows), max(rows)
            for row in range(min_row, max_row + 1):
                if self.board.grid[row][col].letter is None:
                    return False

                # Sprawdzenie sąsiadów
                if self.words_on_board:
                    neighbors = self.get_neighbors_horizontally(row, col)
                    if not any(neighbor.letter is not None for neighbor in neighbors):
                        return False

        return True

    def get_word_at(self, x, y, direction):
        word = ""
        x_start_pos = x
        y_start_pos = y
        if direction == "horizontal":
            while x > 0 and self.board.grid[y][x - 1].letter:
                x -= 1
            x_start_pos = x
            while x < 15 and self.board.grid[y][x].letter:
                word += self.board.grid[y][x].letter
                x += 1
        elif direction == "vertical":
            while y > 0 and self.board.grid[y - 1][x].letter:
                y -= 1
            y_start_pos = y
            while y < 15 and self.board.grid[y][x].letter:
                word += self.board.grid[y][x].letter
                y += 1
        return x_start_pos, y_start_pos, word

    def check_words(self):
        if not self.is_constant_straight_line_with_neighbor(self.current_turn_tiles):
            return False, []

        words_and_positions = []
        direction = "horizontal" if len({y for x, y, tile in self.current_turn_tiles}) == 1 else "vertical"
        for x, y, tile in self.current_turn_tiles:
            x, y, main_word = self.get_word_at(x, y, direction)
            if main_word and len(main_word) > 1 and main_word not in [word for word, _, _ in words_and_positions]:
                word_start_pos = (x, y)
                words_and_positions.append((main_word, word_start_pos, direction))

            if direction == "horizontal":
                x, y, vertical_word = self.get_word_at(x, y, "vertical")
                print(f"vertical_word: {vertical_word}")
                if vertical_word and len(vertical_word) > 1 and vertical_word not in [word for word, _, _ in
                                                                                      words_and_positions]:
                    word_start_pos = (x, y)
                    words_and_positions.append((vertical_word, word_start_pos, "vertical"))
            elif direction == "vertical":
                x, y, horizontal_word = self.get_word_at(x, y, "horizontal")
                print(f"horizontal_word: {horizontal_word}")
                if horizontal_word and len(horizontal_word) > 1 and horizontal_word not in [word for word, _, _ in
                                                                                            words_and_positions]:
                    word_start_pos = (x, y)
                    words_and_positions.append((horizontal_word, word_start_pos, "horizontal"))

        print(f"\n===check_words   is_word_valid check for words: {words_and_positions = }")

        # only valid: words_and_positions = [(word, word_start_pos, direction) for word, word_start_pos, direction in
        #                        words_and_positions if word_checker.is_word_valid(word)]
        all_words_valid = all(word_checker.is_word_valid(word) for word, _, _ in words_and_positions)
        return all_words_valid, words_and_positions

    def calculate_word_score(self, word, start_pos, direction):
        print(f"\n===calculate_word_score  word: {word}, start_pos: {start_pos}, direction: {direction} ")
        score = 0
        word_multiplier = 1
        x, y = start_pos

        for letter in word:
            tile = self.board.grid[y][x]
            print(f"letter: {letter}")
            print(f"row:{y} col: {x} modifier: {tile.modifier}")
            letter_score = tile.value
            type(letter_score)
            if tile.modifier == 'L2':
                letter_score *= 2
            elif tile.modifier == 'L3':
                letter_score *= 3
            elif tile.modifier == 'S2':
                word_multiplier *= 2
            elif tile.modifier == 'S3':
                word_multiplier *= 3
            elif tile.modifier == 'S4':
                word_multiplier *= 4

            score += letter_score

            if direction == 'horizontal':
                x += 1
            elif direction == 'vertical':
                y += 1
        print(f'score: {score} word_multiplier: {word_multiplier}')
        return score * word_multiplier



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
