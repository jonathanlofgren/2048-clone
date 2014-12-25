from game import new_game, move_made, possible_moves

""" 2048-playing AI
"""

def best_move(board):
    return possible_moves(board)[0]


def max_score_search(game, depth):
    """ Simple AI that searches the game tree down 
        a given depth and returns the maximum score
        of the leaf nodes at level depth.

        Signature: game, int depth => int score
        Variant: depth
    """
    
    board, score = game
    
    if depth == 0:
        return score
    else:
        new_games = [move_made(game, move) for move in possible_moves(board)]
        return max(max_score_search(g, depth-1) for g in new_games)

if __name__ == "__main__":
    pass
