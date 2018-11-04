def init():
    global square_size
    square_size = 0

    global selected_color
    selected_color = '#008704'

    global moves_color
    moves_color = '#2d7eff'

    global eat_color
    eat_color = '#a30000'

    global dic_algebric_notation
    dic_algebric_notation = {
        'pawn': '',
        'rook': 'R',
        'knight': 'N',
        'bishop': 'B',
        'queen': 'Q',
        'king': 'K'
    }
