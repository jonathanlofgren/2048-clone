from game import move_made, possible_moves, in_board

""" 2048-playing AI
"""


def best_move(game, method = 'score'):
    """
    val should be function game -> int
    """
    board, score = game

    if method == 'score':
        val = lambda board: board[1]
    elif method == 'empty':
        val = empty_squares
    elif method == 'gradient':
        val = gradient_value
    else:
        print('Invalid method given to best_move function')
        exit(1)

    if score < 10000:
        depth = 4
    elif score < 20000:
        depth = 5
    elif score < 30000:
        depth = 7
    else:
        depth = 7
    
    moves = possible_moves(board)
    
    # dict with score for each move
    move_score = dict(zip(moves, [0] * len(moves)))
    
    # search for max score for each move
    for move in moves:
        move_score[move] += max_score_search(move_made(game, move), depth, val)
    
    move = max(move_score, key=move_score.get)
    return move


def max_score_search(game, depth, val):
    """ Simple AI that searches the game tree down
        a given depth and returns the maximum value
        of the leaf nodes at level depth. Value
        is given by the function val(game)

        Signature: game, int depth, function val => int score
        Variant: depth
    """

    board, score = game

    if depth == 0:
        return val(game)
    else:
        new_games = [move_made(game, move) for move in possible_moves(board)]

        if len(new_games) == 0:
            return 0

        return max(max_score_search(g, depth-1, val) for g in new_games)


def get_neighbor_devsum(board):
    size = len(board)

    dev_sum = 0

    for i in range(size):
        for j in range(size):
            if board[i][j]:
                # This is for each non zero square (i,j) in the board

                neighbors = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]
                nonzero_neighbors = [(k, l) for k, l in neighbors if in_board((k, l), size) and board[k][l]]
                square_diffs = [(board[i][j]-board[k][l]) ** 2 for k, l in nonzero_neighbors]
                dev_sum += sum(square_diffs)

    return dev_sum


def best_move_silvia(board):
    moves = possible_moves(board)
    move_std = dict(zip(moves, [0] * len(moves)))

    for move in moves:
        new_board, _ = move_made((board, 0), move)
        move_std[move] = get_neighbor_devsum(new_board)

    move = min(move_std, key=move_std.get)
    return move


def hueristic_value(board):
    """ Some kind of hueristic value for a board setup,
        doesn't seem to work very good.
    """
    top_row = sum(board[0][i] for i in range(4))
    ordered_sum = sum(board[0][i] for i in range(3) if board[0][i] > board[0][i])
    #empty = len([board[i][j] for i in range(4) for j in range(4)])

    return top_row + ordered_sum


def empty_squares(board):
    size = len(board)
    return len([1 for i in range(size) for j in range(size) if not board[i][j]])


if __name__ == "__main__":
    pass
