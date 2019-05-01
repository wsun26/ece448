 #!/usr/bin/python
from mstate import State

def ReadMaze(filename):
	spaces = []
	start = []
	goals = []

	maze = open(filename, 'r')
	line_length = 0
	word = maze.readline()
	word = word.replace('\n', '')
	for char in word:
		line_length += 1

	maze.seek(0)
	maze_read = maze.read()
	maze.close()
	maze_read = maze_read.replace('\n', '')
	for pos, char in enumerate(maze_read):
		if char == ' ' or char == 'P' or char == '.':
			spaces.append(pos)
		if char == 'P':
			start.append(pos)
		if char == '.': 
			goals.append(pos)
	
	state_space = {}
	goals_blank = [0 for x in goals]
	for space in spaces:
		if space%line_length<line_length-1 and space+1 in spaces:
			if(state_space.has_key(space)):
				state_space[space] += [space+1]
			else:
				state_space[space] = [space+1]
		if space%line_length>0 and space-1 in spaces:
			if(state_space.has_key(space)):
				state_space[space] += [space-1]
			else:
				state_space[space] = [space-1]
		if space+line_length in spaces:
			if(state_space.has_key(space)):
				state_space[space] += [space+line_length]
			else:
				state_space[space] = [space+line_length]
		if space-line_length in spaces:
			if(state_space.has_key(space)):
				state_space[space] += [space-line_length]
			else:
				state_space[space] = [space-line_length]
	return (state_space,start[0],goals,line_length)


def DrawMaze(sol, filename, line_length):
	maze = open(filename, 'r')
	maze_read = maze.read()
	maze.close()
	maze_read = list(maze_read.replace('\n', ''))
	cur_char = '0'
	for pos in sol: 
		if maze_read[pos] == '.':
			cur_char = CharCount(cur_char)
			maze_read[pos] = cur_char
	for pos in sol:
		if maze_read[pos] == ' ':
			maze_read[pos] = '.'
	maze_sol = open('sol_maze.txt', 'w+')
	for posi, item in enumerate(maze_read):
		if(posi%line_length == 0 and posi != 0):
			maze_sol.write('\n')
		maze_sol.write('%s' %item)

def CharCount(cur_char):
#while(cur_char!='Z'):
	cur_char=chr(ord(cur_char)+1)
	if(ord(cur_char) == ord('9')+1):
		cur_char = 'a'
	elif(ord(cur_char)==ord('z')+1):
		cur_char = 'A'
	return cur_char