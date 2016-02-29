from game import move_made, possible_moves, in_board
import numpy as np

""" 2048-playing AI
"""

linear_gradient = np.array([
        [1.00, 0.83, 0.66, 0.50],
        [0.83, 0.66, 0.50, 0.33],
        [0.66, 0.50, 0.33, 0.17],
        [0.50, 0.33, 0.17, 0.00]
    ])
linear_gradient = linear_gradient.reshape(linear_gradient.size)
exp_gradient = np.exp(linear_gradient)


def best_move(game, method='score'):
    """
    val should be function game -> int
    """
    board, score = game

    if method == 'score':
        def val(g):
            return g[1]
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
    """
    if depth == 0:
        return val(game)

    new_games = [move_made(game, move) for move in possible_moves(game)]

    if len(new_games) == 0:
        return 0

    return max(max_score_search(g, depth - 1, val) for g in new_games)


def move_made_all(game, move):
    """ Returns every possible outcome of doing the given move
        on the given game. Returns a list of the following form:
        [(p1, g1), (p2, g2), ..., (pn, gn)]
        where p are probabilities of the corresponding game.
    """
    new_game = move_made(game, move, place_new=False)
    board, score = new_game

    # find zeros in board
    ivals, jvals = np.nonzero(board == 0)
    zero_count = len(ivals)

    prob2 = 0.9 * 1.0 / zero_count
    prob4 = 0.1 * 1.0 / zero_count

    games = []
    for i, j in zip(ivals, jvals):
        b2, b4 = board.copy(), board.copy()
        b2[i][j], b4[i][j] = 2, 4
        games.append((prob2, (b2, score)))
        games.append((prob4, (b4, score)))

    return games


def expectimax(game, depth, value_function):
    """ Searches the game tree down to given depth
        to find the maximum expected value of
        value_function. value_function takes the game
        at the leaf nodes and returns a number value.

        Returns tuple (value, move) with the expected value
        and the maximizing move.
    """

    # base case: reached depth
    if depth == 0:
        return value_function(game), 'null'

    possible = possible_moves(game)

    # base case: no more moves
    if not possible:
        return value_function(game), 'null'

    # get the possible outcomes of each possible move
    expanded = [(move, move_made_all(game, move)) for move in possible]

    move_value = []
    # calculate expected value of each possible move
    for move, games in expanded:
        value = sum(p * expectimax(g, depth - 1, value_function)[0] for p, g in games)
        move_value.append((value, move))

    return max(move_value)


def expectimax_move(game, method='score'):
    """ Wrapper function for expectimax that
        just returns the best move according to
        a choice of method.
    """

    if method == 'score':
        def val(g):
            return g[1]
    elif method == 'empty':
        val = empty_squares
    elif method == 'gradient':
        val = gradient_value
    else:
        print('Invalid method given to expectimax function')
        exit(1)

    _, move = expectimax(game, 2, val)
    return move


def gradient_value(game):
    board, _ = game
    scale = 100

    # element-wise multiplication and sum
    return scale * np.dot(board.reshape(board.size), exp_gradient)


def get_neighbor_devsum(board):
    size = len(board)

    dev_sum = 0

    for i in range(size):
        for j in range(size):
            if board[i][j]:
                # This is for each non zero square (i,j) in the board

                neighbors = [(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]
                nonzero_neighbors = [(k, l) for k, l in neighbors if in_board((k, l), size) and board[k][l]]
                square_diffs = [(board[i][j] - board[k][l]) ** 2 for k, l in nonzero_neighbors]
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
    # empty = len([board[i][j] for i in range(4) for j in range(4)])

    return top_row + ordered_sum


def empty_squares(board):
    return board.size - np.count_nonzero(board)


if __name__ == "__main__":
    pass
