from Piece import *


class Queen(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'queen', color, board)

    def search_possible_moves(self):
        # a queen is a mix between a bishop and a rook
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dir in directions:
            self.check_line(dir)
