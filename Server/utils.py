import numpy as np
from tensorflow.keras.models import load_model
from chess import Board, QUEEN, BISHOP, ROOK, PAWN, KNIGHT

board = Board()

ma1 = None
ma2 = None
mn1 = None
mn2 = None

game_board = None
init_board = None

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
nums = ['1', '2', '3', '4', '5', '6', '7', '8']

capt, cast = False, False

def load_assets():

    global ma1
    global ma2
    global mn1
    global mn2
    global init_board

    init_board = np.load('../Model/board.npy')

    ma1 = load_model('../Model/model__alpha1.model')
    ma2 = load_model('../Model/model__alpha2.model')
    mn1 = load_model('../Model/model__num1.model')
    mn2 = load_model('../Model/model__num2.model')

    print('Assets loaded Successfully...')

def new_game():

    global game_board
    global capt
    global cast

    game_board = init_board

    capt, cast = False, False
    print('New Game Started')

def push_move_to_board(move):
    alpha1 = alpha.index(move[0])
    alpha2 = alpha.index(move[2])
    num1 = 7 - nums.index(move[1])
    num2 = 7 - nums.index(move[3])
    p = 0
    for i in range(12):
        if game_board[i, num1, alpha1] == 1:
            p = i
            break

    game_board[i, num1, alpha1] = 0
    for i in range(12):
        if game_board[i, num2, alpha2] == 1:
            game_board[i, num2, alpha2] = 0
            break

    game_board[p, num2, alpha2] = 1
    board.push_san(move)

def get_preds():

    b = np.append(game_board.copy(), 1)
    q = bin(board.pieces_mask(QUEEN, 0))
    bi = bin(board.pieces_mask(BISHOP, 0))
    kn = bin(board.pieces_mask(KNIGHT, 0))
    r = bin(board.pieces_mask(ROOK, 0))
    p = bin(board.pieces_mask(PAWN, 0))

    total = 0
    for c in q[2:]:
        total += int(c)
    b = np.append(b, total)
                
    total = 0
    for c in bi[2:]:
        total += int(c)
    b = np.append(b, total/2)

    total = 0
    for c in kn[2:]:
        total += int(c)
    b = np.append(b, total/2)

    total = 0
    for c in r[2:]:
        total += int(c)
    b = np.append(b, total/2)

    total = 0
    for c in p[2:]:
        total += int(c)
    b = np.append(b, total/8)

    b = np.append(b, board.is_check())
                
    b = np.append(b, [capt, cast])

    b = b.reshape(1, 777)
    alpha1 = ma1.predict(b)[0]
    num1 = mn1.predict(b)[0]
    alpha2 = ma2.predict(b)[0]
    num2 = mn2.predict(b)[0]

    return alpha1, num1, alpha2, num2

def get_best_move():
    
    alpha1, num1, alpha2, num2 = get_preds()

    final_move = ''
    max_points = 0.0

    for move in board.legal_moves:
        out = 0
        move = str(move)
        out += alpha1[alpha.index(move[0])] + num1[nums.index(move[1])] + alpha2[alpha.index(move[2])] + num2[nums.index(move[3])]
        
        if out > max_points:
            max_points = out
            final_move = move

    push_move_to_board(final_move)

    return final_move

if __name__ == '__main__':
    load_assets()
    new_game()
    while board.is_game_over() == False:
        print(board)
        print(f"model played: {get_best_move()}")
        print(board)
        move = input("Enter the move: ")
        push_move_to_board(move)
