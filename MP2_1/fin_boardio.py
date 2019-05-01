#! /user/python/bin


def printtofile(filename, solution, nodes_exp, positions, time):
	board = open(filename, 'w+')
	for y in range(0, 9):
		for x in range(0, 9):
			board.write(solution[y][x])
		board.write('\n')
	board.write('\n')
	for pos in positions:
		board.write(pos[0]+', '+str(pos[1])+', '+str(pos[2])+': '+pos[3]+'\n')
	board.write('\n')
	board.write('Nodes Expanded: '+str(nodes_exp)+'\n')
	board.write('Time Taken: '+str(time))
	board.close()