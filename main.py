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
