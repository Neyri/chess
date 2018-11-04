import settings
from tkinter import *
from PIL import ImageTk, Image


class Piece():
    def __init__(self, i, j, type, color, board):
        self.type = type
        self.color = color
        self.i = i
        self.j = j
        self.init_image()
        self.possible_moves = []
        self.can_eat = []
        self.previous_cells = []
        self.board = board
        self.has_moved = False
        self.eating = None

    def __repr__(self):
        return '{} {} at cell {}{}'.format(self.color, self.type, chr(97 + self.j), 8 - self.i)

    def move_to(self, cell):
        # overloaded for the king
        self.previous_cells.append((self.i, self.j))
        self.board.board[self.i][self.j].piece = None
        self.i = cell[0]
        self.j = cell[1]
        if self.board.board[self.i][self.j].piece:
            self.eating = self.board.board[self.i][self.j].piece
            # print(self, ' eats ', self.eating)
        else:
            self.eating = None
        self.board.board[self.i][self.j].piece = self
        self.possible_moves = []
        self.can_eat = []
        if not self.has_moved:
            self.has_moved = True

    def cancel_move(self):
        cell = self.previous_cells.pop()
        if self.eating:
            self.board.board[self.i][self.j].piece = self.eating
        else:
            self.board.board[self.i][self.j].piece = None
        self.i = cell[0]
        self.j = cell[1]
        self.board.board[self.i][self.j].piece = self
        self.search_possible_moves()
        if len(self.previous_cells) == 0:
            self.has_moved = False

    def get_filename(self):
        return "img\\" + self.type + "_" + self.color + ".png"

    def init_image(self):
        filename = self.get_filename()
        image = Image.open(filename)
        image = image.resize(
            (int(settings.square_size), int(settings.square_size)))
        photo = ImageTk.PhotoImage(image)
        self.image = photo

    def check_line(self, direction):
        # direction is a tuple ex: (-1,1)
        for n in range(1, 8):
            if self.i + n * direction[0] < 0 or self.i + n * direction[0] >= 8\
                    or self.j + n * direction[1] < 0 or self.j + n * direction[1] >= 8:
                break
            if self.board.board[self.i + n * direction[0]][self.j + n * direction[1]].piece:
                if self.board.board[self.i + n * direction[0]][self.j + n * direction[1]].piece.color != self.color:
                    self.possible_moves.append(
                        (self.i + n * direction[0], self.j + n * direction[1]))
                    self.can_eat.append(
                        (self.i + n * direction[0], self.j + n * direction[1]))
                break
            else:
                self.possible_moves.append(
                    (self.i + n * direction[0], self.j + n * direction[1]))

    def render(self, canvas):
        x = (self.j + 1 / 2) * settings.square_size
        y = (self.i + 1 / 2) * settings.square_size
        img = canvas.create_image(x, y, anchor=CENTER, image=self.image)
