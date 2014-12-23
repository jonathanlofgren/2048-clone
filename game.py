import random, math

direction = {'up': (1,0), 'right': (0,-1), 'down':(-1,0), 'left':(0,1)}

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
    
    if len(empty) > 0:
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
    added = True    # makes sure we only do one add per cell
   
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

    # pad newcells to compare to oldcells
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

     
def in_board((i,j), size):
    """ True if (i,j) is a valid position in board of size size. """
    return i > -1 and j > -1 and i < size and j < size


def possible_moves(board):
    """ Returns a list of the possible moves
        on board that change the game state.
        Ex: moves(b) = ['left', 'up']
    """
    size = len(board)
    moves = set()

    b = lambda i,j: board[i][j]
    
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
              
                left  = (i, j-1)
                right = (i, j+1)
                up    = (i-1, j)
                down  = (i+1, j)
              
                # check if the neighbors cells are empty or same number
                if in_board(left,size):
                    if not b(*left) or b(*left) == b(i,j):
                        moves.add('left')
                
                if in_board(right,size):
                    if not b(*right) or b(*right) == b(i,j):
                        moves.add('right')

                if in_board(up,size):
                    if not b(*up) or b(*up) == b(i,j):
                        moves.add('up')

                if in_board(down,size):
                    if not b(*down) or b(*down) == b(i,j):
                        moves.add('down')

    return list(moves)
