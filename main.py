import numpy as np
import random
import pygame
import sys
import math
# Dimensions of board
ROW_COUNT = 6
COLUMN_COUNT = 7
# function that create the board fill in zero by shape of row_count and column_count
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board
# function that responsible of drop the piece in specific place
# it take the row and column and set piece in this place
def drop_piece(board, row, col, piece):
	board[row][col] = piece
#this is a bool function that takes in a board array and an integer col
#it check is move is valid or not 
#if the row is empty "value is 0 " the move is true else false
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0
# function called get_next_open_row that takes in a board array and an integer col
# and returns the first open row in the col column of the board.
# to iterate through each row in the col column from top to bottom using a for loop,
# searching for the first empty row in the col column. 
# If the function finds an empty row, it returns the row number, otherwise it doesn't return any value.
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r
# that print the board
# The function uses the np.flip() function from the NumPy library to flip the board vertically,
# so that the last row of the board is printed first. 
# The value 0 is passed to np.flip() to indicate the vertical dimension of the array (rows).
def print_board(board):
	print(np.flip(board, 0))
#check winner
def winning_move(board, piece):
    # بتشوف بالعرض يعني يرجاله 
	# Check horizontal locations for win
    # this is two nested loop 
    # The outer loop is used to determine the starting column c to begin checking for a win,
    # so that it does not search for a win in a column that has less than four columns
    # The reason why the for loop iterates over COLUMN_COUNT-3 instead of COLUMN_COUNT
    # is to avoid accessing elements that are outside the bounds of the board array.
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

    # بتشوف بالطول يعني يرجاله 
	# Check vertical locations for win
    # this is two nested loop 
    #The outer loop is used to iterate through each column c on the board.
    # so that it does not search for a win in a column that has less than four columns
    # The reason why the for loop iterates over ROW_COUNT-3 instead of ROW_COUNT
    # is to avoid accessing elements that are outside the bounds of the board array.
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
    #  / بشوف القطر اللي علي اليمين القطر ده   
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
    # \ القطر ده 
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
			
     #check 4 pieces to calc the score 
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	# It checks if the window contains four, three, or two pieces of the player's piece,
	# and adds corresponding points to the score.
	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
# If the window contains three pieces of the opponent's piece and one empty position,
# it subtracts points from the score. The function returns the final score.
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	# This line get the values in the center column of the board and stores them in center_array.
	# The [:, COLUMN_COUNT//2] notation is used to extract the values in all rows of the center column.
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	# This line counts the number of frequancy of the given piece in the center_array 
	# and stores the result in center_count.
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	# iterate over each row of theboard and get a four-position window for each starting position in that row.
	# For each window,it calls the evaluate_window function to calculate the score for that window
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	# These lines iterate over each column of the board and extract a four-position window for each starting position in that column.
	# For each window it calls the evaluate_window function to calculate the score for that window.
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
# These lines iterate over each diagonal window that starts from the top-left corner of the board and extract a four-position window
	# for each starting position in that diagonal.
	# For each window, it calls the evaluate_window function to calculate the score for that window.
	
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)
# These lines iterate over each diagonal window that starts from the top-right corner of the board and extract a four-position window 
	# for each starting position in that diagonal. For each window,
	# it calls the evaluate_window function to calculate the score for that window.

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score
# This line checks if any of the following conditions are true:
# winning_move(board, PLAYER_PIECE) returns True, meaning that the player has won the game.
# winning_move(board, AI_PIECE) returns True, meaning that the AI has won the game.
# len(get_valid_locations(board)) == 0 returns True, meaning that there are no more valid moves to make on the board.
# If any of these conditions are true, then the game is in a terminal state and the function returns True.
# Otherwise, the function returns False, indicating that the game is not yet over.
def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# The minimax function is a recursive function that implements the minimax algorithm for determining the best move for the AI player
# the function takes a game board, a search depth, alpha and beta values for check the best move,
# and a boolean value indicating whether the current player is maximizing or minimizing.
def minimax(board, depth, alpha, beta, maximizingPlayer):
	#These lines get a list of all valid moves that can be made on the board
	# and check if the current state of the game is a terminal state.
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	#This line checks if the depth of the search has reached zero or if the current state of the game is a terminal state.
	# If either of these conditions is true, the function returns the score for the current state of the game.
	if depth == 0 or is_terminal:			
	#If the current state of the game is a terminal state,
		if is_terminal:
			 
	#the function returns a score of 100000000000000 if the AI player has wonthe game
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
	#, -10000000000000 if the human player has won the game,
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			# or 0 if the game is a draw. 
			else: # Game is over, no more valid moves
				return (None, 0)
	# If the depth of the search has reached zero,
	# the function returns the score for the current state of the game for the AI player.
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	#If the current player is the AI player and is maximizing, the function initializes the value to negative infinity 
	# and selects a random valid move.
	if maximizingPlayer:
	# It then loops through all valid moves and simulates dropping the AI player's piece in each column 
	# to evaluate the score for each move. It then selects the move with the highest score 
	# and returns the column and the score for that move.
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
		# The alpha-beta pruning technique is used to speed up the search 
		# by pruning branches that are known to lead to suboptimal results.
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
	# If the current player is the human player and is minimizing,
	# the function initializes the value to positive infinity and selects a random valid move.
	# It then loops through all valid moves and simulates dropping the human player's piece in each column 
	# toevaluate the score for each move.
	# It then selects the move with the lowest score and returns the column and the score for that move.
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
	# The alpha-beta pruning technique is used to speed up the search 
	# by pruning branches that are known to lead to suboptimal results.		
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
	
	# These lines iterate over each column in the board and check if the column is a valid location to drop a piece.
	# The is_valid_location function is used to check if a given column is a valid location.
	# If a column is valid, it is added to the valid_locations list.
	
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	# These lines get a list of all valid locations on the board
	# initialize the best_score variable to a very low number
	# and select a random column from the valid_locations list as the initial best_col.
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	#These lines iterate over all the valid locations on the board and simulate dropping the player's piece in each column 
	# to evaluate the score for each move.
	# It then selects the move with the highest score and returns the column for that move.
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


