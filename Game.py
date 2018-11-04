from tkinter import *
from Board import *
from PromotionButton import *


class Game():

    def __init__(self):
        self.window = Tk()
        self.window.title("Martin's Chess Game")

        # chess canvas
        width = 512
        height = 512
        self.canvas = Canvas(self.window, width=width +
                             1, height=height + 1, bd=2)
        settings.square_size = width / 8

        # frame to contain info and buttons
        self.right_frame = Frame(self.window)
        self.right_frame.pack(side=RIGHT, padx=10, pady=10)
        # new game button
        self.new_game_button = Button(self.right_frame, text="New Game",
                                      command=self.new_game)
        self.new_game_button.pack()

        # start a new game
        self.new_game()

        # moves played
        self.moves_played = Label(
            self.right_frame, text=self.text_moves)
        self.moves_played.pack(pady=20)

        # informations
        self.informations = Label(
            self.right_frame, text=self.text_info)
        self.informations.pack(pady=20)
        self.display_info('')

        # pack everything up
        self.window.mainloop()

    def new_game(self):
        self.gameover = False
        self.board = Board(self)
        self.board.render()
        self.canvas.bind("<Button-1>", self.new_click)
        self.canvas.pack(side=TOP, padx=5, pady=5)
        self.text_moves = "List of moves"
        self.text_info = "Informations"
        # should we enable the click
        self.frozen = False

    def new_click(self, event):
        if not self.board.mate and not self.frozen:
            self.board.click(event)
            prev_moves = self.board.prev_moves
            self.update_moves_played(prev_moves)
        elif self.frozen:
            print('choose a piece to promote your pawn into')
        else:
            self.frozen = True
            print("it's gameover, you can start a new game if you want")

    def display_info(self, text):
        self.text_info = 'Informations \n' + text
        self.informations['text'] = self.text_info

    def update_moves_played(self, prev_moves):
        if len(prev_moves) == 0:
            self.text_moves = "List of moves"
        else:
            self.use_algebric_notation(prev_moves)
        self.moves_played['text'] = self.text_moves
        # self.moves_played.pack(pady=20)

    def use_algebric_notation(self, prev_moves):
        # prev_moves format:
        # [type, color, i, j]
        self.text_moves = "List of moves"
        for i in range(len(prev_moves)):
            nb_turn = str(i // 2 + 1)
            piece = settings.dic_algebric_notation[prev_moves[i][0]]
            column = chr(97 + prev_moves[i][2][1])
            row = str(8 - prev_moves[i][2][0])
            if i % 2 == 0:
                self.text_moves += '\n' + nb_turn + ' ' + piece + column + row
            else:
                self.text_moves += ' ' + piece + column + row

    def promotion(self, piece):
        chosen = None
        self.frozen = True
        window = Tk()
        window.title("Promotion")

        # frame to contain info and buttons
        frame = Frame(window, width=20)
        frame.pack(side=RIGHT, padx=10, pady=10)

        def chose(name):
            chosen = name
            self.board.promote(piece, chosen)
            window.destroy()
            self.frozen = False

        # queen button
        queen_button = PromotionButton(frame, text=u"\u265b Queen",
                                       command=lambda: chose(Queen))
        queen_button.pack()
        # rook button
        rook_button = PromotionButton(frame, text=u"\u265c Rook",
                                      command=lambda: chose(Rook))
        rook_button.pack()
        # bishop button
        bishop_button = PromotionButton(frame, text=u"\u265d Bishop",
                                        command=lambda: chose(Bishop))
        bishop_button.pack()
        # knight button
        knight_button = PromotionButton(frame, text=u"\u265e Knight",
                                        command=lambda: chose(Knight))
        knight_button.pack()
