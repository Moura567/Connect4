import numpy as np
import random
import pygame
import sys
import math

#BLUE = (0,0,255)
color3 = (30,30,40)
color1 =(42, 97, 255)
color2 = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

difficulty = ""

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

valid_difficulty = False
while not valid_difficulty:
    try:
        difficulty = int(input("Choose the difficulty level (1: Easy, 2: Medium, 3: Hard): "))
        if difficulty in [1, 2, 3]:
            valid_difficulty = True
        else:
            print("Invalid difficulty level. Please choose 1, 2, or 3.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
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
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
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
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
    depth = 5  # Adjust the depth of the minimax algorithm as per your preference

    if difficulty == 1:
        # Random move for easy difficulty
        valid_locations = get_valid_locations(board)
        return random.choice(valid_locations)

    if difficulty == 2:
        # Medium difficulty: Randomize score for some variation
        valid_locations = get_valid_locations(board)
        best_score = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            score += random.randint(-3, 3)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    if difficulty == 3:
        # Hard difficulty: Use minimax algorithm with alpha-beta pruning
        column, _ = minimax(board, depth, -math.inf, math.inf, True)
        return column



def draw_board(board, winner=None):
	screen.blit(background_image, (0, 0))
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			#pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, color3, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, color1, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, color2, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

	if winner is not None:
	   if winner == PLAYER_PIECE:
		   text = "Player 1 wins!"
		   color = color1
	   else:
		   text = "Player 2 wins!"
		   color = color2
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
    ##These lines check for the "QUIT" event, which is triggecolor1
    ## when the user clicks the "X" button in the top right corner of the game window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        ## The pygame.MOUSEMOTION event is triggecolor1 when the user moves the mouse on the game window.
        ## These lines update the position of the player's piece on the screen to follow the mouse movement.
        ## A color3 rectangle is drawn over the top of the previous position of the player's piece to erase it,
        ## and a new color1 circle is drawn at the new position of the player's piece.
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, color3, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, color1, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, color3, (0, 0, width, SQUARESIZE))
        # print(event.pos)
        # Ask for Player 1 Input
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
            label = myfont.render("Game Over", 1, color1)
            screen.blit(label, (150,10))
            game_over = True

    pygame.display.update()
