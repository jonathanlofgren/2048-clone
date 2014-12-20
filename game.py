import random

direction = [(0,1), (1,0), (0,-1), (-1,0)]

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

def make_move(game, move):
    """ Makes the given move on the given game.
        Returns the game with the updated board
        and score.
    """
    
    board, score = game
    size = len(board)

    def collapse(start, direction):
        i, j = start
        di, dj = direction
        
        # collapse each cell one at a time
        while i < size and j < size:
            
            if not board[i][j]: # skip if its an empty cell
                continue
            
            ii, jj = i+di, j+dj # cell right before

            while ii and jj and ii < size and jj < size: # while in board
                val = board[ii][jj]
    

def print_board(board):
    for row in board:
        print row


if __name__ == "__main__":
    b, s = new_game(4)
    print_board(b)

    place_random(b)
    print_board(b)
    
