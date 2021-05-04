#TODO import numpy
from math import inf as infinity
import copy

COMP = 1
HUMAN = -1

def children_states(state):
    turn = HUMAN if sum(state) == 0 else COMP
    children = []
    for i in range(9):
        if state[i] == 0:
            children +=  [tuple(state[j]  if j!=i else turn for j in range(9))]
    return children


Three_aligned = {(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)}

def eval_win(state):
    for (i,j,k) in Three_aligned:
        if state[i] != 0 and state[i] == state[j] and state[j] == state[k]:
            return state[i]
    for i in range(9):
        if state[i] == 0:
            return children_states(state)
    return 0

Start = tuple(0 for i in range(9))
Tree = {}
Scores = {}

def fill_tree(current_state):
    children = eval_win(current_state)
    if type(children) == list:
        for child_state in children:
            if child_state not in Tree:
                fill_tree(child_state)
    Tree[current_state] = children


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
    global Start
    move = -1
    print(f'Human turn ["O"]')
    print_board()

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            can_move = (Start[move-1] == 0)

            if not can_move:
                print('Bad move')
                move = -1
            else:
                Start = tuple(Start[j]  if j!=move-1 else -1 for j in range(9))
        except (EOFError, KeyboardInterrupt):
            print('error')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def choose_move():
    global Start,Scores
    children = eval_win(Start)
    best = -infinity
    best_index = None
    for c in children:
        if Scores[c] > best:
            best = Scores.get(c)
            best_index = c
    Start = best_index;


def ai_turn(): 
    global board
    print(f'AI turn ["X"]')
    print_board()
    choose_move()


def minimax(current_state):
    global Scores
    children = eval_win(current_state)
    if type(children) == int:
        score = children
    else:
        turn = HUMAN if sum(current_state) == 0 else COMP
        score = -turn
        for child_state in children:
            if child_state not in Tree:
                minimax(child_state)
            score = max(score,Scores[child_state]) if turn == COMP else min(score,Scores[child_state])
    Tree[current_state] = children
    Scores[current_state] = score


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def print_board():
    global Start
    print("*************")
    for x in range(0,3):
        s = "|"
        for y in range(0,3):
            if Start[x*3+y] == 0:
                s+="   "
            elif Start[x*3+y] == COMP :
                s+=" X "
            else:
                s+=" O "
            s+="|"
        print(s)
        print("*************")


def main():

    #fill_tree(Start)
    print("********************")
    minimax(Start)
    print(len(Tree))
    print(len(Scores))

    while (type(eval_win(Start)) != int):
    
        human_turn()
        if(type(eval_win(Start)) == int):
            break
        #todo lecture arbre faire un choix
        ai_turn()
    print_board();
    score = eval_win(Start)
    if score == 1:
        print("AI win")
    elif score == -1:
        print("Human win")
    else:
        print("draw")

if __name__ == '__main__':
    main()