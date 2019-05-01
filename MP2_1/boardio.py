#!/usr/bin/python
def readBoard(filename):

	board = open(filename, 'r')
	board_read = board.read()
	board.close()
	board_read = board_read.replace('\n', '')
	letter_bank = []
	for pos, char in enumerate(board_read):
		if(char != '_'):
			letter_bank += [char]
	board_space = [['_' for x in range(9)] for y in range(9)]
	for pos, char in enumerate(board_read):
		if(char != '_'):
			board_space[pos/9][pos%9] = char
	#for i in range(len(board_space)):
	#	print board_space[i]
	#print board_space
	return letter_bank, board_space