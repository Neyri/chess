from Piece import *


class Pawn(Piece):
    def __init__(self, i, j, color, board):
        Piece.__init__(self, i, j, 'pawn', color, board)
        if self.color == 'black':
            self.direction = 1
            self.startin_row = 1
        else:
            self.direction = -1
            self.startin_row = 6

    # def move_to(self, cell):
    #     Piece.move_to(self, cell)

    def search_possible_moves(self):
        # a pawn moves forward 1 cell
        # except at the beginning where he can move forward 2 cells
        # if there is a piece forward in diagonal he can eat if it's the opposite color
        if self.i + self.direction >= 0 and self.i + self.direction < 8:
            if not self.board.board[self.i + self.direction][self.j].piece:
                self.possible_moves.append((self.i + self.direction, self.j))
                # moves 2 row
                if self.i == self.startin_row and not self.board.board[self.i + self.direction * 2][self.j].piece:
                    self.possible_moves.append(
                        (self.i + self.direction * 2, self.j))
            # grab a piece
            if self.j < 7 and self.board.board[self.i + self.direction][self.j + 1].piece\
                    and self.board.board[self.i + self.direction][self.j + 1].piece.color != self.color:
                self.possible_moves.append(
                    (self.i + self.direction, self.j + 1))
                self.can_eat.append((self.i + self.direction, self.j + 1))
            if self.j > 0 and self.board.board[self.i + self.direction][self.j - 1].piece\
                    and self.board.board[self.i + self.direction][self.j - 1].piece.color != self.color:
                self.possible_moves.append(
                    (self.i + self.direction, self.j - 1))
                self.can_eat.append((self.i + self.direction, self.j - 1))

            # en passant
            self.en_passant(1)
            self.en_passant(-1)

    def en_passant(self, dir):
        # c stands for condition
        if self.j + dir < 8 and self.j + dir >= 0 \
                and self.board.board[self.i][self.j + dir].piece:
            # the piece next to me is a pawn of the opposite color
            c3 = self.board.board[self.i][self.j +
                                          dir].piece.color != self.color
            c4 = self.board.board[self.i][self.j + dir].piece.type == 'pawn'
            c5 = len(self.board.prev_moves) > 0
            c6 = len(self.board.board[self.i]
                     [self.j + dir].piece.previous_cells) > 0
            if c3 and c4 and c5 and c6:
                # has the pawn moved 2 rows previously
                previous_position = self.board.board[self.i][self.j +
                                                             dir].piece.previous_cells[-1]
                # it's actually the current move
                current_position = self.board.prev_moves[-1]
                c6 = previous_position[0] == self.i + 2 * self.direction
                # has this pawn moved previously
                c7 = previous_position[1] == current_position[2][1]
                if c6 and c7:
                    self.possible_moves.append(
                        (self.i + self.direction, self.j + dir))
                    self.can_eat.append(
                        (self.i + self.direction, self.j + dir))
