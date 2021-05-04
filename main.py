#TODO import numpy
from math import inf as infinity

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
dict_etat = {}
dict_lien = {}
dict_score = {}
COMP = 1
HUMAN = -1

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells

def score(state):
    if wins(state, COMP):
        score = +1
        #print("Computer win")
    elif wins(state, HUMAN):
        score = -1
        #print("Human win")
    else:
        score = 0
        #print("NULL")

    return score

def human_turn():
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    print(f'Human turn ["O"]')
    print_board(board)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('error')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

def init_tree():
    
    dict_etat[0] = [ [0,0,0], [0,0,0], [0,0,0] ]
    dict_lien[0] = []
    minimax(HUMAN, 0)

def ai_turn(): 
    move = 1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    print(f'AI turn ["X"]')
    print_board(board)

    x, y, z =  minimax(board, len(empty_cells(board)), COMP)
    set_move(x, y, COMP)

def minimax(player, netat):
    d = len(empty_cells(dict_etat[netat]))

    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if d == 0 or game_over(dict_etat[netat]):
        
        dict_score[netat] = score(dict_etat[netat])
        return 
    
    for cell in empty_cells(dict_etat[netat]):
        x, y = cell[0], cell[1]
        tmp = dict_etat[netat]
        tmp[x][y] = player

        if tmp in dict_etat.values():
            child = [key  for (key, value) in dict_etat.items() if value == tmp]
            #return
        else:
            child = len(dict_etat)
            dict_etat[child] = tmp
            dict_lien[netat].append(child)
            dict_lien[child] = []
            minimax(-player,child)

        

        if player == COMP:
            if dict_score.get(child) > best[2]:
                best = dict_score.get(child)  # max value
        else:
            if dict_score.get(child) < best[2]:
                best = dict_score.get(child)  # min value

    dict_score[netat] = best


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def print_board(state):
    print("*************")
    for x, row in enumerate(state):
        s = "|"
        for y, cell in enumerate(row):
            if state[x][y] == 0:
                s+="   "
            elif state[x][y] == COMP :
                s+=" X "
            else:
                s+=" O "
            s+="|"
        print(s)
        print("*************")



# player can be human or AI
def wins(state, player):
    
    board_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in board_state:
        return True
    else:
        return False

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def main():

    #print_board(board)
    init_tree()
    print(len(dict_etat))
    while (not game_over(board)) and (len(empty_cells(board)) != 0):
        human_turn()
        #todo lecture arbre faire un choix
        ai_turn()
    if score(board) == 1:
        print("AI win")
    elif score(board) == -1:
        print("Human win")
    else:
        print("draw")
    print("Taille arbre : " + str(len(dict_etat)))

if __name__ == '__main__':
    main()