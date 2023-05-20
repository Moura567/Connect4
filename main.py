import numpy as np
import random
import pygame
import sys
import math
color1 = (0,0,255)
color3 = (30,30,40)
color2 =(42, 97, 255)
color4 = (255,255,255)

# Dimensions of board
ROW_COUNT = 6
COLUMN_COUNT = 7


PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (width,height))

# function that create the board fill in zero by shape of row_count and column_count
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# function that responsible of drop the piece in specific place
# it take the row and column and set piece in this place
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# this is a bool function that takes in a board array and an integer col
# it check is move is valid or not
# if the row is empty "value is 0 " the move is true else false
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


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


# check winner
def winning_move(board, piece):
    # بتشوف بالعرض يعني يرجاله
    # Check horizontal locations for win
    # this is two nested loop
    # The outer loop is used to determine the starting column c to begin checking for a win,
    # so that it does not search for a win in a column that has less than four columns
    # The reason why the for loop iterates over COLUMN_COUNT-3 instead of COLUMN_COUNT
    # is to avoid accessing elements that are outside the bounds of the board array.
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # بتشوف بالطول يعني يرجاله
    # Check vertical locations for win
    # this is two nested loop
    # The outer loop is used to iterate through each column c on the board.
    # so that it does not search for a win in a column that has less than four columns
    # The reason why the for loop iterates over ROW_COUNT-3 instead of ROW_COUNT
    # is to avoid accessing elements that are outside the bounds of the board array.
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    #  / بشوف القطر اللي علي اليمين القطر ده
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    # \ القطر ده
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


# check 4 pieces to calc the score
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
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    # This line counts the number of frequancy of the given piece in the center_array
    # and stores the result in center_count.
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    # iterate over each row of theboard and get a four-position window for each starting position in that row.
    # For each window,it calls the evaluate_window function to calculate the score for that window
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    # These lines iterate over each column of the board and extract a four-position window for each starting position in that column.
    # For each window it calls the evaluate_window function to calculate the score for that window.
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    # These lines iterate over each diagonal window that starts from the top-left corner of the board and extract a four-position window
    # for each starting position in that diagonal.
    # For each window, it calls the evaluate_window function to calculate the score for that window.

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # These lines iterate over each diagonal window that starts from the top-right corner of the board and extract a four-position window
    # for each starting position in that diagonal. For each window,
    # it calls the evaluate_window function to calculate the score for that window.

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
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
    # These lines get a list of all valid moves that can be made on the board
    # and check if the current state of the game is a terminal state.
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    # This line checks if the depth of the search has reached zero or if the current state of the game is a terminal state.
    # If either of these conditions is true, the function returns the score for the current state of the game.
    if depth == 0 or is_terminal:
        # If the current state of the game is a terminal state,
        if is_terminal:

            # the function returns a score of 100000000000000 if the AI player has wonthe game
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            # , -10000000000000 if the human player has won the game,
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            # or 0 if the game is a draw.
            else:  # Game is over, no more valid moves
                return (None, 0)
        # If the depth of the search has reached zero,
        # the function returns the score for the current state of the game for the AI player.
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    # If the current player is the AI player and is maximizing, the function initializes the value to negative infinity
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
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            # The alpha-beta pruning technique is used to speed up the search
            # by pruning branches that are known to lead to suboptimal results.
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
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
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
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
    # These lines iterate over all the valid locations on the board and simulate dropping the player's piece in each column
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

def draw_board(board, winner=None):
	screen.blit(background_image, (0, 0))
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			#pygame.draw.rect(screen, color1, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, color3, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, color2, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, color4, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

	if winner is not None:
	   if winner == PLAYER_PIECE:
		   text = "Player 1 wins!"
		   color = color2
	   else:
		   text = "Player 2 wins!"
		   color = color4
	   label = myfont.render(text, 1, color)
	   text_bg = pygame.Rect(30, 0, 200, 50)
	   #pygame.draw.rect(screen, color3, text_bg)
	   screen.blit(label, (40, 10))
	   pygame.display.flip()
	   pygame.time.wait(3000)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont(None, 75)

turn = random.randint(PLAYER, AI)

while not game_over:
    ##These lines check for the "QUIT" event, which is triggecolor2
    ## when the user clicks the "X" button in the top right corner of the game window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        ## The pygame.MOUSEMOTION event is triggecolor2 when the user moves the mouse on the game window.
        ## These lines update the position of the player's piece on the screen to follow the mouse movement.
        ## A color3 rectangle is drawn over the top of the previous position of the player's piece to erase it,
        ## and a new color2 circle is drawn at the new position of the player's piece.
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, color3, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, color2, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, color3, (0, 0, width, SQUARESIZE))
        # Ask for Player 1 Input
        ## If it is the human player's turn, a random column is selected for the player to drop their piece.
        ## The code waits for 1 second using `pygame.time.wait(1000)` to simulate the player thinking about their move.
        if turn == PLAYER:
            col = random.randint(0, COLUMN_COUNT - 1)
            pygame.time.wait(1000)
            ## check if the place that player choose is valid to play in
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                ##The code then checks if the player has won the game by calling the `winning_move` function.
                ## If theplayer has won, a message is displayed on the screen using the `myfont.render`
                ## and `screen.blit` functions, and the `game_over` variable is set to `True`
                if winning_move(board, PLAYER_PIECE):
                    draw_board(board,winner=PLAYER_PIECE)
                    game_over = True

                print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2
			# # Ask for Player 2 Input
			##If it is the AI player's turn and the game is not over,
			## the AI selects the best move to make by calling the `pick_best_move` function.
			## The code waits for 1 second using `pygame.time.wait(1000)` to simulate the AI thinking about its move.
			## If the selected column is avalid location, the AI player drops its piece into the lowest empty row in that column.
			## The code then checks if the AI player has won the game by calling the `winning_move` function. If the AI player has won,
			## a message is displayed on the screen using the `myfont.render` and `screen.blit` functions,
			## and the `game_over` variable is set to `True`.
			## The `print_board` and `draw_board` functions are called to display the updated game board on the screen.

        if turn == AI and not game_over:
            pygame.time.wait(1000)
            col = pick_best_move(board, AI_PIECE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    draw_board(board,winner=AI_PIECE)
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(300)
            break

        if is_terminal_node(board):
            label = myfont.render("Game Over", 1, color2)
            screen.blit(label, (150,10))
            game_over = True

    pygame.display.update()
