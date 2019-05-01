#! /user/python/bin
from boardio import *
from bankio import *
from fin_boardio import *
import time

def solveSudoku(board_space, letter_bank, word_bank, nodes_exp, position_return):
	count = 0
	for i in range(len(board_space)):
		if('_' in board_space[i]): break
		count += i
	if(count == 8): return (board_space, nodes_exp, position_return)

	board_space_cp = [row[:] for row in board_space]
	letter_bank_cp = letter_bank[:]
	word_bank_cp = word_bank[:]
	position_return_cp = [row[:] for row in position_return]

	if(word_bank == []): return (board_space, nodes_exp, position_return_cp)

	for pos in boardPos(word_bank_cp[0], board_space_cp):
		position_return_cp += [pos]
		if(pos[0] == 'H'):
			for word_pos in range(len(pos[3])):
				board_space_cp[pos[1]][pos[2]+word_pos] = (pos[3])[word_pos] #place letter into board space
				letter_bank_cp += (pos[3])[word_pos] #add word to letter bank
			nodes_exp += 1
			result, nodes_exp, position_return_cp = solveSudoku(board_space_cp, letter_bank_cp, word_bank_cp[1:], nodes_exp, position_return_cp) #recursive sudoku solve

			if(result != []): return (result, nodes_exp, position_return_cp) #check if letter bank is empty
	
			position_return_cp = [row[:] for row in position_return]
			board_space_cp = [row[:] for row in board_space]
			letter_bank_cp = letter_bank[:]

		if(pos[0] == 'V'):
			for word_pos in range(len(pos[3])):
				board_space_cp[pos[1]+word_pos][pos[2]] = (pos[3])[word_pos] #place letter into board space
				letter_bank_cp += (pos[3])[word_pos] #add word to letter bank
			nodes_exp += 1
			result, nodes_exp, position_return_cp = solveSudoku(board_space_cp, letter_bank_cp, word_bank_cp[1:], nodes_exp, position_return_cp) #recursive sudoku solve

			if(result != []): return (result, nodes_exp, position_return_cp) #check if letter bank is empty

			position_return_cp = [row[:] for row in position_return]
			board_space_cp = [row[:] for row in board_space]
			letter_bank_cp = letter_bank[:]	

	return ([], nodes_exp, position_return_cp)

def boardPos(word, board_space): 

	pos = []
	y = 0
	while(y < 9):
		x = 0
		while(len(word) <= 9-x):
			pos.append(['H', y, x, word, 0])
			x += 1
		y += 1
	x = 0
	while(x < 9):
		y = 0
		while(len(word) <= 9-y):
			pos.append(['V', y, x, word, 0])
			y += 1
		x += 1
	i = 0
	remove = []
	for position in pos:

		if(position[0] == 'H'):
			for word_position in range(len(word)):

				if(board_space[position[1]][position[2]+word_position] != '_'):
					if(board_space[position[1]][position[2]+word_position] != word[word_position]):
						remove += [position]
					else: position[4] += 1
				
				else:
					x_it_range = range(0, 9)
					y_it_range = range(0, 9)

					for x in x_it_range[:position[2]]+x_it_range[position[2]+len(word):]:
						if(word[word_position] == board_space[position[1]][x]):
							remove += [position]
					for y in y_it_range[:position[1]]+y_it_range[position[1]+1:]:
						if(word[word_position] == board_space[y][position[2]+word_position]):
							remove += [position]

		if(position[0] == 'V'):
			for word_position in range(len(word)):

				if(board_space[position[1]+word_position][position[2]] != '_'):
					if(board_space[position[1]+word_position][position[2]] != word[word_position]):
						remove += [position]
					else: position[4] += 1

				else:
					x_it_range = range(0, 9)
					y_it_range = range(0, 9)
					for x in x_it_range[:position[2]]+x_it_range[position[2]+1:]:
						if(word[word_position] == board_space[position[1]+word_position][x]):
							remove += [position]
					for y in y_it_range[:position[1]]+y_it_range[position[1]+len(word):]:
						if(word[word_position] == board_space[y][position[2]]):
							remove += [position]
	for rem in remove:
		if rem in pos:
			pos.remove(rem)
	remove = []

	for position in pos:

		if(position[0] == 'H'):

			for word_position in range(len(word)):

				y_min, y_max = 6, 9
				if(position[1]<3): y_min, y_max = 0, 3
				elif(position[1]<6): y_min, y_max = 3, 6

				x_min, x_max = 6, 9
				if(position[2]+word_position<3): x_min, x_max = 0, 3
				elif(position[2]+word_position<6): x_min, x_max = 3, 6

				for y in range(y_min, y_max):
					for x in range(x_min, x_max):
						if(board_space[y][x] == word[word_position]): #!!!
							if(y != position[1] and x != position[2]+word_position):
								remove += [position]

		if(position[0] == 'V'):

			for word_position in range(len(word)):

				y_min, y_max = 6, 9
				if(position[1]+word_position<3): y_min, y_max = 0, 3
				elif(position[1]+word_position<6): y_min, y_max = 3, 6

				x_min, x_max = 6, 9
				if(position[2]<3): x_min, x_max = 0, 3
				elif(position[2]<6): x_min, x_max = 3, 6

				for y in range(y_min, y_max):
					for x in range(x_min, x_max):
						if(board_space[y][x] == word[word_position]): #!!!
							if(y != position[1]+word_position and x != position[2]):
								remove += [position]
	for rem in remove:
		if rem in pos:
			pos.remove(rem)
	pos.sort(lambda x, y: cmp(x[4], y[4]))
	pos.reverse()
	return pos


letter_bank, board_space = readBoard('blankboard.txt')
word_bank = readBank('blankbank.txt')
time_dif = time.time()
solution, nodes_exp, positions = solveSudoku(board_space, letter_bank, word_bank, 0, [])
time_dif = time.time() - time_dif
printtofile('blankoutput.txt', solution, nodes_exp, positions, time_dif)