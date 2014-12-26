from game import new_game, move_made, possible_moves

""" 2048-playing AI
"""

def best_move(game):
    board, score = game
    
    if score < 10000:
        depth = 4
    elif score < 20000:
        depth = 5
    elif score < 30000:
        depth = 6
    else:
        depth = 7
    
    moves = possible_moves(board)
    
    # dict with score for each move
    move_score = dict(zip(moves, [0] * len(moves)))
    
    # search for max score for each move
    for move in moves:
        move_score[move] += max_score_search(move_made(game, move), depth)
    
    move = max(move_score.iterkeys(), key = lambda k: move_score[k])
    return move

def hueristic_value(board):
    """ Some kind of hueristic value for a board setup,
        doesn't seem to work very good.
    """
    top_row = sum(board[0][i] for i in range(4))
    ordered_sum = sum(board[0][i] for i in range(3) if board[0][i] > board[0][i])
    #empty = len([board[i][j] for i in range(4) for j in range(4)])

    return top_row + ordered_sum


def max_score_search(game, depth):
    """ Simple AI that searches the game tree down 
        a given depth and returns the maximum score
        of the leaf nodes at level depth.

        Signature: game, int depth => int score
        Variant: depth
    """
    
    board, score = game
    
    if depth == 0:
        return score #+ hueristic_value(board)
    else:
        new_games = [move_made(game, move) for move in possible_moves(board)]
        
        if len(new_games) == 0:
            return 0
        
        return max(max_score_search(g, depth-1) for g in new_games)

if __name__ == "__main__":
    pass
