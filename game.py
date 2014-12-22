import random, math
import sys, pygame
from pygame.locals import *
pygame.init()

direction = {'up': (1,0), 'right': (0,-1), 'down':(-1,0), 'left':(0,1)}

def color(n):
    """ Return RGB color for cell value n. """

    val = 255-20*math.log(n,2)
    if val < 0:
        val = 0

    return (255, val, val)


def new_game(size):
    """ Returns a new game with two random cells placed. """

    board = [[0 for _ in range(size)] for _ in range(size)]
    place_random(board)
    place_random(board)

    return (board, 0)


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
    """ Collapses a row/column in board, starting from
        the position start and walking in the given direction.
    """

    size = len(board)   
    i, j = start
    di, dj = direction
    score = 0

    newcells = []
    oldcells = []
    added = True     # makes sure we only do one add per cell
   
    # collect new updated cells to newcells
    while i > -1 and j > -1 and i < size and j < size:
        cell = board[i][j]
        oldcells.append(cell)

        if cell != 0:
            if not added and newcells[-1] == cell:
                newcells[-1] *= 2
                score += newcells[-1]
                added = True
            else:
                newcells.append(cell)
                added = False

            board[i][j] = 0
        
        i, j = i+di, j+dj

    # insert the new cells back in board
    i, j = start
    for c in newcells:
        board[i][j] = c
        i, j = i+di, j+dj

    # pad the newcells to compare to oldcells
    newcells += [0] * (len(oldcells) - len(newcells))

    return (score, newcells != oldcells)

def make_move(board, move):
    """ Makes the given move on the given board
        and returns the score gained by the move.
        move should be 'left','right','up' or 'down'
    """
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

    result = [collapse(board, s, cdir) for s in start]
    
    # check if anything was changed by the move
    if any(change for _,change in result):    
        place_random(board)
        
    return sum(score for score,_ in result)
     

class GameView:
    def __init__(self):
        self.size = 600, 450
        self.myfont = pygame.font.SysFont("monospace", 35)
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048')
        self.background = pygame.Surface(self.size)
        self.background.fill((255,255,255))
        self.window.blit(self.background, (0,0))
        pygame.display.flip()
        
    def color(self, n):
        """ Return RGB color for cell value n. """
        
        val = 255-20*math.log(n,2)
        if val < 0:
            val = 0
        return (255, val, val)


    def draw(self, board, score):
        size = len(board)
        
        self.background.fill((20,20,20))
        
        # draw the cells
        for i in range(size):
            for j in range(size):
                val = board[i][j]
                if val: 
                    xpos, ypos = 10 + 110*j, 10 + 110*i
                    cell = pygame.Surface((100,100))
                    cell.fill(self.color(val))
                    text = self.myfont.render(str(val), 1, (0,0,0))
                    tx, ty = text.get_size()

                    cell.blit(text, (50-tx/2,50-ty/2))
                    self.background.blit(cell, (xpos,ypos))
                    
        # draw score text
        label = self.myfont.render("Score:", 1, (255,255,255))
        scoretxt = self.myfont.render(str(score), 1, (255,255,255))
        self.background.blit(label, (450,10))
        self.background.blit(scoretxt, (450,50))

        # update display
        self.window.blit(self.background, (0,0))
        pygame.display.flip()


def main():
    
    view = GameView()    
    board, score = new_game(4)
    view.draw(board,score)
    
    while True:
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
            view.draw(board, score)

if __name__ == "__main__":
    main()
  
