import settings


class Square():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        if (i + j) % 2 == 0:
            # yellow
            self.color = '#ffff99'
        else:
            # brown
            self.color = '#996633'
        self.piece = None
        self.moves = False
        self.selected = False
        self.eattable = False

    def select(self, game):
        if not self.piece:
            return
        self.selected = True
        self.piece.search_possible_moves()
        for square in self.piece.possible_moves:
            game.board[square[0]][square[1]].moves = True
        for square in self.piece.can_eat:
            game.board[square[0]][square[1]].eattable = True
        game.selected_square = self

    def render(self, canvas):
        x0 = self.j * settings.square_size
        y0 = self.i * settings.square_size
        x1 = (self.j + 1) * settings.square_size
        y1 = (self.i + 1) * settings.square_size
        color = self.color
        if self.eattable:
            color = settings.eat_color
        elif self.moves:
            color = settings.moves_color
        elif self.selected:
            color = settings.selected_color
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        if self.piece:
            self.piece.render(canvas)
        if self.j == 0:
            text = canvas.create_text(
                15, y1 - 20, text=str(8 - (self.i)), anchor="ne", fill="black", font=('Arial', '12', 'bold'))
            # canvas.itemconfig(text, text=chr(96 + self.i + 1))
        if self.i == 7:
            text = canvas.create_text(
                x1 - 10, y1 - 20, text=chr(97 + self.j), anchor="nw", fill="black", font=('Arial', '12', 'bold'))
            # canvas.itemconfig(text)

    def render_labels(self):
        for i in range(8):
            text = self.canvas.create_text(
                i * settings.square_size, 10, anchor="nw")
            self.canvas.itemconfig(text, text=i)
