from Piece import *


class Rook(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'rook', color, board)

    def search_possible_moves(self):
        # a rook moves vertically or horizontally
        # its possible directions are (-1, 0), (0, -1), (0, 1), (1, 0)
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        for dir in directions:
            self.check_line(dir)
