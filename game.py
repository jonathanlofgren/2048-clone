import random
import sys, pygame
from pygame.locals import *
pygame.init()

direction = {'up': (1,0), 'right': (0,1), 'down':(-1,0), 'left':(0,-1)}

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

    # keep set of already added cells so as to limit
    # a cell to being added at most once
    added = set()

    while i < size and j < size:
        
        if not board[i][j]: # skip if its an empty cell
            continue
                
        ii, jj = i+di, j+dj # cell right before

        move = 0
        while ii and jj and ii < size and jj < size: # go in the opposite direction
                
            if not board[ii][jj]: # zero, keep checking
                move = 1
                continue
            elif  board[ii][jj] == board[i][j]: # add cells
                board[ii][jj] += board[i][j]
                board[i][j] = 0
                score += board[ii][jj]
                move = 0
                break
            else: # different valued cell
                break

            ii, jj = ii+di, jj+dj # go to next cell
        
        if move:
            board[ii][jj] = board[i][j]
            board[i][j] = 0

        i, j = i-di, j-dj

    return score

def make_move(game, move):
    """ Makes the given move on the given game.
        Returns the game with the updated board
        and score.
    """
    board, score = game
    size = len(board)
    cdir = direction[move]
    
    if move is 'left':
        start = ((i, 1) for i in range(size))
    elif move is 'up':
        start = ((1, i) for i in range(size))
    elif move is 'right':
        start = ((i, size-2) for i in range(size))
    elif move is 'down':
        start = ((size-2, i) for i in range(size))

    for s in start:
        score += collapse(board, s, cdir)

    return (board, score)
  
    
                

def print_board(board):
    for row in board:
        print row


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
    main()
        
