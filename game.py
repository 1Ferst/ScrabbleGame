import pygame
from board import GameBoard
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = GameBoard()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_index = 0

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.board.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
