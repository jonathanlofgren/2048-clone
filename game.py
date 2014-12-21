import random
import sys, pygame
from pygame.locals import *
pygame.init()

direction = {'up': (1,0), 'right': (0,-1), 'down':(-1,0), 'left':(0,1)}

def new_game(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    score = 0
    return (board, score)


def place_random(board):
    """ Places a value of 2 or 4 at a random
        empty place in the board.
    """
    value = 2 + 2 * (random.random() < 0.1)
    ind = range(len(board))
    empty = [(i,j) for i in ind for j in ind if not board[i][j]]
    i, j = random.choice(empty)
    board[i][j] = value


def collapse(board, start, direction):
    size = len(board)   
    i, j = start
    di, dj = direction
    score = 0

    nonzero = []
    # get the nonzero cells to l
    while i > -1 and j > -1 and i < size and j < size:
        if board[i][j]:
            nonzero.append(board[i][j])
            board[i][j] = 0
        i, j = i+di, j+dj

    i = 0
    # do the adding of equal cells
    while i < len(nonzero)-1:
        if nonzero[i] == nonzero[i+1]:
            nonzero[i], nonzero[i+1] = 2*nonzero[i], 0
            score += nonzero[i]
            i += 2
        else:
            i += 1
    
    # again get only the nonzero cells
    nonzero = [c for c in nonzero if c != 0]

    # insert the new cells back in board
    i, j = start
    for c in nonzero:
        board[i][j] = c
        i, j = i+di, j+dj

    return score

def make_move(board, move):
    """ Makes the given move on the given board
        and returns the score gained by the move.
        move should be 'left','right','up' or 'down'
    """
    score = 0
    size = len(board)
    cdir = direction[move]
    
    if move is 'left':
        start = ((i, 0) for i in range(size))
    elif move is 'up':
        start = ((0, i) for i in range(size))
    elif move is 'right':
        start = ((i, size-1) for i in range(size))
    elif move is 'down':
        start = ((size-1, i) for i in range(size))

    for s in start:
        score += collapse(board, s, cdir)

    return score
  
    
                

def print_board(board):
    for row in board:
        print row
    print ""

class GameView:
    def __init__(self):
        size = width, height = 450, 450
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(size)
        self.background.fill((255,255,255))
        self.window.blit(self.background, (0,0))
        pygame.display.flip()

def main():
    
    view = GameView()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return


if __name__ == "__main__":
    #main()
        
    b, s = new_game(4)
    print_board(b)

    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)
    place_random(b)

    print_board(b)
    

    s = make_move(b, 'down')

    print_board(b)
