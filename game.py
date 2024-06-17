import pygame
from board import Board
from bag import Bag
from player_rack import PlayerRack
import random
import word_checker
import time


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.bag = Bag()
        self.player_rack = PlayerRack(self.bag)
        self.player_score = 0
        self.player_rack.refill_rack()
        self.dragging_tile = None
        self.dragging_offset_x = 0
        self.dragging_offset_y = 0
        self.words_on_board = set()
        self.current_turn_tiles = []
        self.selected_tile = None
        self.messages = []
        self.message_duration = 5

    def set_message(self, message):
        timestamp = time.time()
        self.messages.append((message, timestamp))

    def draw_game(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        self.board.draw_player_score(self.screen, self.player_score)
        self.player_rack.draw(self.screen)
        self.board.draw_confirm_button(self.screen)
        self.draw_messages()
        if self.dragging_tile:
            self.dragging_tile.draw(self.screen, (pygame.mouse.get_pos()[0] - self.dragging_offset_x, pygame.mouse.get_pos()[1] - self.dragging_offset_y))
        pygame.display.flip()

    def draw_messages(self):
        y_offset = 10
        for message, timestamp in self.messages:
            elapsed_time = time.time() - timestamp
            if elapsed_time < self.message_duration:
                font = pygame.font.Font(None, 36)
                text = font.render(message, True, (255, 255, 255))
                text_rect = text.get_rect(center=(300, 20 + y_offset))
                pygame.draw.rect(self.screen, (255, 0, 0), (text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20))
                self.screen.blit(text, text_rect)
                y_offset += text_rect.height + 20
            else:
                self.messages.pop(0)

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
        all_words_valid, words_and_positions = self.check_words()
        if any([word for word, _, _ in words_and_positions if word in self.words_on_board]):
            self.set_message('Słowo się powtarza')
        if all_words_valid:
            total_turn_score = 0
            for word, start_pos, direction in words_and_positions:
                word_score = self.calculate_word_score(word, start_pos, direction)
                total_turn_score += word_score
                self.words_on_board.add(word)
                self.set_message(f'Za słowo {word} otrzymujesz {word_score} punktów')

            self.player_score += total_turn_score
            for x, y, tile in self.current_turn_tiles:
                tile.modifier = None
        else:
            for x, y, tile in self.current_turn_tiles[:]:
                self.player_rack.rack.append(tile)
                self.current_turn_tiles.remove((x, y, tile))
                self.board.remove_tile(tile)
            if self.current_turn_tiles:
                self.set_message('Kafelki wróciły na stojak')

        self.player_rack.refill_rack()
        self.dragging_tile = None
        self.current_turn_tiles = []

    def return_tile_to_rack(self, tile):
        tile_tuple = next((t for t in self.current_turn_tiles if t[2] == tile), None)

        if tile_tuple:
            self.player_rack.rack.append(tile)
            self.current_turn_tiles.remove(tile_tuple)
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
        if len([tile[0] for tile in tiles]) < 2 and not self.words_on_board:
            self.set_message('Przynajmniej dwuliterowe słowa')
            return False

        rows = [tile[1] for tile in tiles]
        cols = [tile[0] for tile in tiles]

        if not self.words_on_board and (7, 7) not in [(tile[0], tile[1]) for tile in tiles]:
            self.set_message('Pierwsze słowo musi być ulokowane na środku')
            return False

        is_straight = len(set(rows)) == 1 or len(set(cols)) == 1
        if not is_straight:
            self.set_message('Kafelki nie są ułożone w linii prostej')
            return False

        if len(set(rows)) == 1:
            row = rows[0]
            min_col, max_col = min(cols), max(cols)
            for col in range(min_col, max_col + 1):
                if self.board.grid[row][col].letter is None:
                    self.set_message('W słowie jest luka')
                    return False
                if self.words_on_board:
                    neighbors = self.get_neighbors_vertically(row, col)
                    if not any(neighbor.letter is not None for neighbor in neighbors):
                        self.set_message('Słowo musi łączyć się z literą z poprzednich rund')
                        return False

        else:
            col = cols[0]
            min_row, max_row = min(rows), max(rows)
            for row in range(min_row, max_row + 1):
                if self.board.grid[row][col].letter is None:
                    self.set_message('W słowie jest luka')
                    return False
                if self.words_on_board:
                    neighbors = self.get_neighbors_horizontally(row, col)
                    if not any(neighbor.letter is not None for neighbor in neighbors):
                        self.set_message('Słowo musi łączyć się z literą z poprzednich rund')
                        return False

        return True

    def get_word_at(self, x, y, direction):
        word = ''
        x_start_pos = x
        y_start_pos = y
        if direction == 'horizontal':
            while x > 0 and self.board.grid[y][x - 1].letter:
                x -= 1
            x_start_pos = x
            while x < 15 and self.board.grid[y][x].letter:
                word += self.board.grid[y][x].letter
                x += 1
        elif direction == 'vertical':
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
        direction = 'horizontal' if len({y for x, y, tile in self.current_turn_tiles}) == 1 else 'vertical'
        for x, y, tile in self.current_turn_tiles:
            x, y, main_word = self.get_word_at(x, y, direction)
            if main_word and len(main_word) > 1 and main_word not in [word for word, _, _ in words_and_positions]:
                word_start_pos = (x, y)
                words_and_positions.append((main_word, word_start_pos, direction))

            if direction == 'horizontal':
                x, y, vertical_word = self.get_word_at(x, y, 'vertical')
                if vertical_word and len(vertical_word) > 1 and vertical_word not in [word for word, _, _ in
                                                                                      words_and_positions]:
                    word_start_pos = (x, y)
                    words_and_positions.append((vertical_word, word_start_pos, 'vertical'))
            elif direction == 'vertical':
                x, y, horizontal_word = self.get_word_at(x, y, 'horizontal')
                if horizontal_word and len(horizontal_word) > 1 and horizontal_word not in [word for word, _, _ in
                                                                                            words_and_positions]:
                    word_start_pos = (x, y)
                    words_and_positions.append((horizontal_word, word_start_pos, 'horizontal'))

        all_words_valid = True
        for word, _, _ in words_and_positions:
            if not word_checker.is_word_valid(word):
                all_words_valid = False
                self.set_message(f'Słowo {word} nie znajduje się w słowniku')

        return all_words_valid, words_and_positions

    def calculate_word_score(self, word, start_pos, direction):
        score = 0
        word_multiplier = 1
        x, y = start_pos

        for letter in word:
            tile = self.board.grid[y][x]
            letter_score = tile.value
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
                            for x, y, tile in self.current_turn_tiles[:]:
                                self.player_rack.rack.append(tile)
                                self.current_turn_tiles.remove((x, y, tile))
                                self.board.remove_tile(tile)
                        elif self.check_exchange_button_click(event.pos):
                            if self.bag.tiles:  # Zobaczenie czy bag nie jest pusty
                                for tile in self.player_rack.rack[:]:
                                    self.bag.tiles.append(tile)
                                    self.player_rack.remove_tile(tile)

                                for x, y, tile in self.current_turn_tiles[:]:  # W trakcie wymiany, wrzucenie z planszy do worka liter z tury
                                    self.bag.tiles.append(tile)
                                    self.current_turn_tiles.remove((x, y, tile))
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
                                self.dragging_tile.modifier = self.board.grid[grid_y][grid_x].modifier
                                self.board.place_tile(grid_x, grid_y, self.dragging_tile)
                                self.current_turn_tiles.append((grid_x, grid_y, self.dragging_tile))
                                if self.dragging_tile.letter == '_':
                                    self.selected_tile = self.dragging_tile
                            else:
                                self.player_rack.rack.append(
                                    self.dragging_tile)  # Wrzucenie kafelka z powrotem na stojak
                        else:
                            self.player_rack.rack.append(self.dragging_tile)
                        self.dragging_tile = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_tile:
                        self.draw_game()

                elif event.type == pygame.KEYDOWN:
                    if self.selected_tile:
                        if event.unicode.isalpha() and len(event.unicode) == 1:
                            self.selected_tile.letter = event.unicode.upper()
                            self.selected_tile = None
                    if event.key == pygame.K_RETURN:  # Naciśnięto klawisz Enter
                        self.player_rack.refill_rack()
                        self.current_turn_tiles = []
            self.draw_game()

        pygame.quit()
