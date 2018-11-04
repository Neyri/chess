from Piece import *


class Bishop(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'bishop', color, board)

    def search_possible_moves(self):
        # a bishop moves in diagonal
        # its possible directions are (-1,-1), (-1,1), (1,-1), (1,1)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dir in directions:
            self.check_line(dir)
