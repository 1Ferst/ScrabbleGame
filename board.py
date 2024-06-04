import pygame
import copy
from tile import Tile


class GameBoard:
    def __init__(self):
        row_1 = [
            Tile(modifier="S4"), Tile(), Tile(), Tile(modifier="L2"), Tile(),
            Tile(), Tile(), Tile(modifier="S3"), Tile(), Tile(),
            Tile(), Tile(modifier="L2"), Tile(), Tile(), Tile(modifier="S4")
        ]

        row_2 = [
            Tile(), Tile(modifier="S2"), Tile(), Tile(), Tile(),
            Tile(modifier="L3"), Tile(), Tile(), Tile(), Tile(modifier="L3"),
            Tile(), Tile(), Tile(), Tile(modifier="S2"), Tile()
        ]

        row_3 = [
            Tile(), Tile(), Tile(modifier="S2"), Tile(), Tile(),
            Tile(), Tile(modifier="L2"), Tile(), Tile(modifier="L2"), Tile(),
            Tile(), Tile(), Tile(modifier="S2"), Tile(), Tile()
        ]

        row_4 = [
            Tile(modifier="L2"), Tile(), Tile(), Tile(modifier="S2"), Tile(),
            Tile(), Tile(), Tile(modifier="L2"), Tile(), Tile(),
            Tile(), Tile(modifier="S2"), Tile(), Tile(), Tile(modifier="L2")
        ]

        row_5 = [
            Tile(), Tile(), Tile(), Tile(), Tile(modifier="S2"),
            Tile(), Tile(), Tile(), Tile(), Tile(),
            Tile(modifier="S2"), Tile(), Tile(), Tile(), Tile()
        ]

        row_6 = [
            Tile(), Tile(modifier="L3"), Tile(), Tile(), Tile(),
            Tile(modifier="L3"), Tile(), Tile(), Tile(), Tile(modifier="L3"),
            Tile(), Tile(), Tile(), Tile(modifier="L3"), Tile()
        ]

        row_7 = [
            Tile(), Tile(), Tile(modifier="L2"), Tile(), Tile(),
            Tile(), Tile(modifier="L2"), Tile(), Tile(modifier="L2"), Tile(),
            Tile(), Tile(), Tile(modifier="L2"), Tile(), Tile()
        ]

        row_8 = [
            Tile(modifier="S3"), Tile(), Tile(), Tile(modifier="L2"), Tile(),
            Tile(), Tile(), Tile(modifier="S2"), Tile(), Tile(),
            Tile(), Tile(modifier="L2"), Tile(), Tile(), Tile(modifier="S3")
        ]

        row_9 = copy.deepcopy(row_7)
        row_10 = copy.deepcopy(row_6)
        row_11 = copy.deepcopy(row_5)
        row_12 = copy.deepcopy(row_4)
        row_13 = copy.deepcopy(row_3)
        row_14 = copy.deepcopy(row_2)
        row_15 = copy.deepcopy(row_1)

        self.board = [
            row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8,
            row_9, row_10, row_11, row_12, row_13, row_14, row_15
        ]

        self.words_on_board = []

        self.letter_bag = ['A']*9 + ['E']*7 + ['I']*8 + ['N']*5 + ['O']*6 + ['R']*4 + ['S']*4 + ['W']*4 + ['Z']*5 + \
                          ['C']*3 + ['D']*3 + ['K']*3 + ['L']*3 + ['M']*3 + ['P']*3 + ['T']*3 + \
                          ['Y']*4 + ['B']*2 + ['G']*2 + ['H']*2 + ['J']*2 + ['Ł']*2 + ['U']*2 + ['Ą']*1 + \
                          ['Ę']*1 + ['F']*1 + ['Ó']*1 + ['Ś']*1 + ['Ż']*1 + ['Ć']*1 + ['Ń']*1 + ['Ź']*1 + ['blank']*2

        self.letter_points = {
            'A': 1, 'E': 1, 'I': 1, 'N': 1, 'O': 1, 'R': 1, 'S': 1, 'W': 1, 'Z': 1,
            'C': 2, 'D': 2, 'K': 2, 'L': 2, 'M': 2, 'P': 2, 'T': 2, 'Y': 2,
            'B': 3, 'G': 3, 'H': 3, 'J': 3, 'Ł': 3, 'U': 3,
            'Ą': 5, 'Ę': 5, 'F': 5, 'Ó': 5, 'Ś': 5, 'Ż': 5,
            'Ć': 6, 'Ń': 7, 'Ź': 9, 'blank': 0
        }



