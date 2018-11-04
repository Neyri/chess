from Piece import *


class King(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'king', color, board)
        self.is_in_chess = False
        self.is_castling = False

    def search_possible_moves(self):
        # a king moves around him
        # is possible cells are (i+1, j), (i+1,j+1), ...
        for k in range(-1, 2):
            for l in range(-1, 2):
                # am i inside the board
                if self.i + k >= 0 and self.i + k < 8 \
                        and self.j + l >= 0 and self.j + l < 8 \
                        and (k != 0 or l != 0):
                    if not self.board.board[self.i + k][self.j + l].piece:
                        self.possible_moves.append((self.i + k, self.j + l))
                    elif self.board.board[self.i + k][self.j + l].piece.color != self.color:
                        self.possible_moves.append((self.i + k, self.j + l))
                        self.can_eat.append((self.i + k, self.j + l))
        if self.can_castle('king_side'):
            self.possible_moves.append((self.i, 6))
        if self.can_castle('queen_side'):
            self.possible_moves.append((self.i, 2))

    def move_to(self, cell):
        # Am I going to castle ?
        if cell[1] - self.j == 2:
            # castle on king size
            self.board.board[self.i][7].piece.move_to((self.i, 5))
            self.is_castling = True
        elif cell[1] - self.j == -2:
            # castle on queen size
            self.board.board[self.i][0].piece.move_to((self.i, 3))
            self.is_castling = True
        else:
            self.is_castling = False
        Piece.move_to(self, cell)

    def is_chess(self, cell=(-1, -1)):
        if cell == (-1, -1):
            cell = (self.i, self.j)
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j].piece \
                        and self.board.board[i][j].piece.color != self.color\
                        and self.board.board[i][j].piece.type != 'king':
                    self.board.board[i][j].piece.search_possible_moves()
                    if cell in self.board.board[i][j].piece.possible_moves:
                        # print(self.board.board[i][j].piece.possible_moves)
                        # print('chess by ', self.board.board[i][j].piece)
                        self.board.board[i][j].piece.possible_moves = []
                        return True
        return False

    def can_castle(self, side):
        # Castling may only be done if the king has never moved the rook involved has never moved,
        # the squares between the king and the rook involved are unoccupied, the king is not in check,
        # and the king does not cross over or end on a square in which it would be in check
        if side == 'queen_side' and self.board.board[self.i][0].piece:
            rook = self.board.board[self.i][0].piece
        elif side == 'king_side' and self.board.board[self.i][0].piece:
            rook = self.board.board[self.i][7].piece

        if side == 'queen_side':
            return (not(self.has_moved or rook.has_moved)
                    # squares between the king and the rook involved are unoccupied
                    and not(self.board.board[self.i][1].piece
                            or self.board.board[self.i][2].piece
                            or self.board.board[self.i][3].piece)
                    # the king does not begin, cross over or end on a square in which it would be in check
                    and not(self.is_chess((self.i, 2))
                            or self.is_chess((self.i, 3))
                            or self.is_chess((self.i, 4))))
        elif side == 'king_side':
            return (not(self.has_moved or rook.has_moved)
                    # squares between the king and the rook involved are unoccupied
                    and not(self.board.board[self.i][6].piece
                            or self.board.board[self.i][5].piece)
                    # the king does not begin, cross over or end on a square in which it would be in check
                    and not(self.is_chess((self.i, 6))
                            or self.is_chess((self.i, 5))
                            or self.is_chess((self.i, 4))))
