from Piece import *


class Knight(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'knight', color, board)

    def search_possible_moves(self):
        # a knight moves around him
        # is possible cells are (i+1, j+2), (i+1,j-2), ...
        all_cells = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1)
        ]
        for k, l in all_cells:
            # am i inside the board
            if self.i + k >= 0 and self.i + k < 8 \
                    and self.j + l >= 0 and self.j + l < 8 \
                    and (k != 0 or l != 0):
                if not self.board.board[self.i + k][self.j + l].piece:
                    self.possible_moves.append((self.i + k, self.j + l))
                elif self.board.board[self.i + k][self.j + l].piece.color != self.color:
                    self.possible_moves.append((self.i + k, self.j + l))
                    self.can_eat.append((self.i + k, self.j + l))
