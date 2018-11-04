import settings
from Square import *
from pieces.Pawn import *
from pieces.Rook import *
from pieces.Knight import *
from pieces.Bishop import *
from pieces.Queen import *
from pieces.King import *
import Game
import datetime


class Board():

    def __init__(self, game):
        self.game = game
        self.canvas = self.game.canvas
        self.board = []
        self.init_squares()
        self.init_pieces()
        self.selected_square = None
        self.prev_moves = []
        self.color_turn = 'white'
        self.mate = False
        self.rendered_square = []
        self.turn = 0

    def init_squares(self):
        # Init the squares
        for i in range(8):
            self.board.append([])
            for j in range(8):
                cell = Square(i, j)
                self.board[i].append(cell)

    def init_pieces(self):
        # Init the pieces
        # black
        self.board[0][0].piece = Rook(0, 0, 'black', self)
        self.board[0][7].piece = Rook(0, 7, 'black', self)
        self.board[0][1].piece = Knight(0, 1, 'black', self)
        self.board[0][6].piece = Knight(0, 6, 'black', self)
        self.board[0][2].piece = Bishop(0, 2, 'black', self)
        self.board[0][5].piece = Bishop(0, 5, 'black', self)
        self.board[0][3].piece = Queen(0, 3, 'black', self)
        self.board[0][4].piece = King(0, 4, 'black', self)
        # white
        self.board[7][0].piece = Rook(7, 0, 'white', self)
        self.board[7][7].piece = Rook(7, 7, 'white', self)
        self.board[7][1].piece = Knight(7, 1, 'white', self)
        self.board[7][6].piece = Knight(7, 6, 'white', self)
        self.board[7][2].piece = Bishop(7, 2, 'white', self)
        self.board[7][5].piece = Bishop(7, 5, 'white', self)
        # self.board[4][2].piece = Bishop(4, 2, 'white', self)
        self.board[7][3].piece = Queen(7, 3, 'white', self)
        # self.board[3][7].piece = Queen(3, 7, 'white', self)
        self.board[7][4].piece = King(7, 4, 'white', self)
        for j in range(8):
            self.board[1][j].piece = Pawn(1, j, 'black', self)
            self.board[6][j].piece = Pawn(6, j, 'white', self)
        # self.board[1][4].piece = Pawn(1, 4, 'white', self)

    def click(self, event):
        self.reset_cells()
        i = int(event.y / settings.square_size)
        j = int(event.x / settings.square_size)
        # if I already have selected a piece
        # and I can move to the new square
        if self.can_make_the_move_to(i, j):
            self.make_the_move_to(i, j)
            # self.render()
        elif self.has_selected_the_right_color(i, j):
            self.reset_pieces()
            self.board[i][j].select(self)
            # self.render()
        self.render()

    def make_the_move_to(self, i, j):
        cell = (i, j)
        piece = self.selected_square.piece
        piece.move_to(cell)
        self.register_move(cell, piece)
        self.check_chess()
        self.selected_square = None
        self.check_promotion(piece)
        self.switch_color_turn()
        self.turn += 1

    def check_promotion(self, piece):
        if piece.type == 'pawn' \
                and (piece.i == 0 or piece.i == 7):
            self.game.display_info('Choose a piece to promote your pawn into')
            self.render()
            self.game.promotion(piece)

    def promote(self, piece, choice):
        i = piece.i
        j = piece.j
        color = piece.color
        self.board[i][j].piece = choice(i, j, color, self)
        self.render()

    def check_chess(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece and self.board[i][j].piece.type == 'king':
                    if self.board[i][j].piece.is_chess():
                        if self.board[i][j].piece.color == self.color_turn:
                            self.game.display_info('you cannot do that')
                            self.cancel_move()
                            self.render()
                        else:
                            self.game.display_info('chess')
                            # is there also chess mate
                            self.check_mate(self.board[i][j].piece)
                        return

    def check_mate(self, king):
        # we are going to check if a move of a piece can remove the check...
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece \
                        and self.board[i][j].piece.color == king.color:
                    piece = self.board[i][j].piece
                    piece.search_possible_moves()
                    for square in piece.possible_moves:
                        # we make the piece move then cancel the move
                        piece.move_to(square)
                        if not king.is_chess():
                            piece.cancel_move()
                            return False
                        piece.cancel_move()
        self.game.display_info('MATE :(')
        self.mate = True

    def cancel_move(self):
        new_cell = self.prev_moves.pop()[2]
        current_square = self.board[new_cell[0]][new_cell[1]]
        current_piece = self.board[new_cell[0]][new_cell[1]].piece
        prev_cell = current_piece.previous_cells.pop()
        prev_square = self.board[prev_cell[0]][prev_cell[1]]
        current_piece.i = prev_square.i
        current_piece.j = prev_square.j
        prev_square.piece = current_piece
        if current_piece.eating:
            current_square.piece = current_piece.eating
        else:
            current_square.piece = None
        self.switch_color_turn()  # to cancel the one in click function

    def has_selected_the_right_color(self, i, j):
        return self.board[i][j].piece \
            and self.board[i][j].piece.color == self.color_turn

    def can_make_the_move_to(self, i, j):
        return self.selected_square and self.selected_square.piece \
            and(i, j) in self.selected_square.piece.possible_moves \
            and self.selected_square.piece.color == self.color_turn

    def register_move(self, new_cell, piece):
        self.prev_moves.append([piece.type, piece.color, new_cell, piece])

    def switch_color_turn(self):
        if self.color_turn == 'white':
            self.color_turn = 'black'
        else:
            self.color_turn = 'white'

    def reset_cells(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j].selected = False
                self.board[i][j].moves = False
                self.board[i][j].eattable = False

    def reset_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece:
                    self.board[i][j].piece.possible_moves = []
                    self.board[i][j].piece.can_eat = []

    def render(self):
        if len(self.prev_moves) == 0:
            # first, we render all the squares
            for j in range(8):
                for i in range(8):
                    self.board[i][j].render(self.canvas)
                    self.rendered_square.append((i, j))
        else:
            # we render only the previous cell, the new one and the piece it ate
            prev_move = self.prev_moves[-1]
            piece = prev_move[3]
            possible_moves = []
            if self.selected_square:
                possible_moves = self.selected_square.piece.possible_moves
            square_to_render = possible_moves + [
                (piece.i, piece.j),
                piece.previous_cells[-1]
            ]
            if piece.eating:
                eatten = piece.eating
                square_to_render.append((eatten.i, eatten.j))
            if piece.type == 'king' and piece.is_castling:
                square_to_render.append((piece.i, 7))
                square_to_render.append((piece.i, 5))
                square_to_render.append((piece.i, 0))
                square_to_render.append((piece.i, 3))
            # we also render again the one we rendered previously
            for (i, j) in (square_to_render + self.rendered_square):
                self.board[i][j].render(self.canvas)
            self.rendered_square = square_to_render
