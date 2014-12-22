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

    cells = []
    added = True

    while i > -1 and j > -1 and i < size and j < size:
        if board[i][j] != 0:
            if not added and cells[-1] == board[i][j]:
                cells[-1] *= 2
                score += cells[-1]
                added = True
            else:
                cells.append(board[i][j])
                added = False

            board[i][j] = 0

        i, j = i+di, j+dj

    # insert the new cells back in board
    i, j = start
    for c in cells:
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
        
    place_random(board)
        
    return score
                  

def print_board(board):
    for row in board:
        print row
    print ""


class GameView:
    def __init__(self):
        self.size = 450, 450
        self.myfont = pygame.font.SysFont("monospace", 40)
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(self.size)
        self.background.fill((255,255,255))
        self.window.blit(self.background, (0,0))
        pygame.display.flip()

    def draw(self, board):
        s = len(board)
        
        self.background.fill((255,255,255))

        for i in range(s):
            for j in range(s):
                
                val = board[i][j]
                if val: 
                    xpos, ypos = 10 + 110*j, 10 + 110*i
                    cell = pygame.Surface((100,100))
                    cell.fill((100,100,100))
                    text = self.myfont.render(str(val), 1, (0,0,0))
                    cell.blit(text, (50,50))
                    self.background.blit(cell, (xpos,ypos))
                    

        self.window.blit(self.background, (0,0))
        pygame.display.flip()


def main():
    
    view = GameView()
    
    board, score = new_game(4)
    place_random(board)
    place_random(board)
    
    view.draw(board)
    
    while 1:
        redraw = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    score += make_move(board, 'left')
                    redraw = True
                if event.key == pygame.K_RIGHT:
                    score += make_move(board, 'right')
                    redraw = True
                if event.key == pygame.K_UP:
                    score += make_move(board, 'up')
                    redraw = True
                if event.key == pygame.K_DOWN:
                    score += make_move(board, 'down')
                    redraw = True
        if redraw:            
            view.draw(board)

if __name__ == "__main__":
    main()
  
