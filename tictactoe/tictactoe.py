"""
Tic Tac Toe Player
"""

import math

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
    player_x = sum(row.count(X) for row in board) # Count how many X's are currently on the board
    player_o = sum(row.count(O) for row in board) # Count how many O's are currently on the board

    print(f"Player X: {player_x}, Player O: {player_o}") # Debug information: show counts of each player

    # If X has more moves, it is O's turn; otherwise X's turn
    if player_x > player_o:
        return O
    
    return X # Otherwise, it is X's turn (X always starts the game)

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set() # Use a set to avoid duplicate moves
    # Loop through all rows
    for i in range(3):
        # Loop through all columns
        for j in range(3):
            # If the current cell is empty, it's a valid move
            if board[i][j] == EMPTY:
                actions_set.add((i, j))
    
    # Debug information: show all available moves
    print(f"Available actions: {actions_set}")
    return actions_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action # Unpack the action into row and column
    # If the chosen cell is not empty, the move is invalid
    if board[i][j] != EMPTY:
        raise ValueError("Invalid move")
    
    new_board = [row.copy() for row in board] # Create a deep copy of the board to preserve the original state
    new_board[i][j] = player(board) # Place the symbol of the current player on the chosen cell
    return new_board # Return the new board with the move applied

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    print("Checking for winner...")

    # Check each row for three identical symbols
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0] # Winner is the symbol in that row
        
    # Check each column for three identical symbols
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col] # Winner is the symbol in that column
    
    # Check top-left to bottom-right diagonal
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    
    # Check top-right to bottom-left diagonal
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None # If no winner is found, return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    print("Checking if game is over...")

    # Check if there is a winner (any row, column, or diagonal)
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return True
        
    # Game also ends if there are no empty cells (draw)
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return True
        
    # If there are no empty cells left, the game is also over (tie)
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return True
    
    # If there are no empty cells left, the game is also over (tie)
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True
    
    return False # Otherwise, the game is still ongoing

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check who the winner is
    if terminal(board):
        x_count = sum(row.count(X) for row in board)
        o_count = sum(row.count(O) for row in board)

        if x_count > o_count:
            return 1  # X wins
        
        elif o_count > x_count:
            return -1  # O wins
        
    return 0  # Tie or game not over


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is already over, no moves can be made
    if terminal(board):
        return None # No moves possible

    current_player = player(board) # Determine which player is about to move
    best_action = None # Placeholder for the best action found

    # Case 1: X’s turn (maximize the score)
    if current_player == X:
        best_value = -math.inf # Start lower than any possible score
        for action in actions(board): # Try all possible moves
            state = result(board, action) # Simulate move
            # If move ends the game, evaluate immediately
            if terminal(state):
                value = utility(state)
            else:
                # Simulate O’s response (minimizing player)
                v = math.inf
                for a2 in actions(state):
                    state2 = result(state, a2)
                    if terminal(state2):
                        temp_val = utility(state2)
                    else:
                        # Simulate X’s next move
                        temp_v = -math.inf
                        for a3 in actions(state2):
                            state3 = result(state2, a3)
                            if terminal(state3):
                                temp_val2 = utility(state3)
                            else:
                                # Deeper recursion could go here (simplified)
                                temp_val2 = utility(state3)  # fallback if not expanding deeper
                            temp_v = max(temp_v, temp_val2)
                        temp_val = temp_v
                    v = min(v, temp_val) # O minimizes score
                value = v
            # Keep track of the action with the best score for X
            if value > best_value:
                best_value = value
                best_action = action

    # Case 2: O’s turn (minimize the score)
    else:
        best_value = math.inf # Start higher than any possible score
        for action in actions(board): # Try all possible moves
            state = result(board, action) # Simulate move
            if terminal(state):
                value = utility(state)
            else:
                # Simulate X’s response (maximizing player)
                v = -math.inf
                for a2 in actions(state):
                    state2 = result(state, a2)
                    if terminal(state2):
                        temp_val = utility(state2)
                    else:
                        # Simulate O’s next move
                        temp_v = math.inf
                        for a3 in actions(state2):
                            state3 = result(state2, a3)
                            if terminal(state3):
                                temp_val2 = utility(state3)
                            else:
                                # Deeper recursion could go here (simplified)
                                temp_val2 = utility(state3) 
                            temp_v = min(temp_v, temp_val2)
                        temp_val = temp_v
                    v = max(v, temp_val) # X maximizes score
                value = v
            # Keep track of the action with the best score for O
            if value < best_value:
                best_value = value
                best_action = action

    # Return the optimal move for the current player
    return best_action
