"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    used_turn_count = 0
    for row in board:
        for element in row:
            if element != None:
                used_turn_count += 1
    return X if (used_turn_count % 2 == 0) else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions_set = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise Exception
    else:
        board_copy = copy.deepcopy(board)
        board_copy[action[0]][action[1]] = player(board)
        return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if won(board, X):
        return X
    elif won(board, O):
        return O
    else:
        return None


# won() returns True if player won, and False if player did not win
def won(board, player):

    # Check for horizontals
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Check for verticals
    for column in range(3):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            return True

    # Check for diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    # Return False if the player did not win
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If any player wins, game is over
    if won(board, X) or won(board, O):
        return True
    else:
        for row in board:
            for element in row:
                # If board is not completely filled up yet (and none of the players won), game is not over
                if element == EMPTY:
                    return False

        # If board is completely filled up, game is over
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Returns set of possible actions
    actions_set = actions(board)

    # If player is X, player will try to maximise value
    if player(board) == X:
        maximum = -999999
        for action in actions_set:
            tmp = min_value(result(board, action))
            if tmp > maximum:
                optimal_action = action
                maximum = tmp

    # If player is O, player will try to minimise value
    else:
        minimum = 999999
        for action in actions_set:
            tmp = max_value(result(board, action))
            if tmp < minimum:
                optimal_action = action
                minimum = tmp

    return optimal_action


def max_value(board):
    if terminal(board):
        return utility(board)
    value = -999999
    for action in actions(board):
        value = max(value, min_value(result(board, action)))

        # Partial pruning
        if value == 1:
            return value

    return value


def min_value(board):
    if terminal(board):
        return utility(board)
    value = 999999
    for action in actions(board):
        value = min(value, max_value(result(board, action)))

        # Partial pruning
        if value == -1:
            return value

    return value
