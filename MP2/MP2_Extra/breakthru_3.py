#!/usr/bin/python
from gamestate_3 import BoardState
import sys
import time
import math

def eval_fn(state,p_color,o_rat,d_rat):
	player = state.getPieces(p_color)
	op_color = 0
	if(p_color == 0):
		op_color = 1
	oppo = state.getPieces(op_color)
	winner = state.getWinner()
	if(winner>=0 and winner!=p_color):
		return -500
	elif(winner>=0 and winner==p_color):
		return 500

	score = 0

	p_max = -1
	p_min = 50

	op_max = -1
	op_min = 50

	p_col = [1 for i in range(10)]
	op_col = [1 for i in range(10)]

	p_col_num = [0 for i in range(10)]
	p_row_num = [0 for i in range(5)]

	op_col_num = [0 for i in range(10)]
	op_row_num = [0 for i in range(5)]

	p_mob = 0
	op_mob = 0

	for p in player:
		p_col[p%10]=0
		p_col_num[p%10]+=1
		#print p
		p_row_num[int(p/10)]+=1
		p_mob+=len(state.getValidMoves(p_color,p))
		if(p>p_max):
			p_max = p
		if(p<p_min):
			p_min = p
	for p in oppo:
		op_col[p%10]=0
		op_col_num[p%10]+=1
		op_row_num[int(p/10)]+=1
		op_mob+=len(state.getValidMoves(op_color,p))
		if(p>op_max):
			op_max = p
		if(p<op_min):
			op_min = p

	p_mob=int(p_mob/len(player))
	op_mob = int(op_mob/len(oppo))


	#Score Pieces Taken:
	#	Max: 16
	score += o_rat*state.getCaptures(p_color)-d_rat*state.getCaptures(op_color)

	#Score Open Columns:
	#	Max: 16
	score+=(o_rat*sum(op_col)-d_rat*sum(p_col))*2

	#Score Closest Pieces:
	#	Max: 7
	#	May not be a good heuristic
	'''if(p_color == 0):
		#Color is white, want closest piece to row 8
		w_close = int(p_max/8)
		b_close = 7-int(op_min/8)
		#score+=(o_rat*w_close-d_rat*b_close)
	elif(p_color == 1):
		#Color is black, want closest piece to row 1
		w_close = int(op_max/8)
		b_close = 7-int(p_min/8)
		#score+=(o_rat*b_close-d_rat*w_close)'''

	#Score H Config:
	#	Max: 24
	p_num_h = 0
	p_sum_h = 0
	op_num_h = 0
	op_sum_h = 0
	for r in p_row_num:
		if(r>=2):
			p_num_h+=1
			p_sum_h+=r
	for r in op_row_num:
		if(r>=2):
			op_num_h+=1
			op_sum_h+=r

	d_h_score = 0
	o_h_score = 0
	if(p_num_h > 0):
		d_h_score = d_rat*int(p_sum_h/p_num_h)
	if(op_num_h > 0):
		o_h_score = o_rat*int(op_sum_h/op_num_h)
	score += (d_h_score)*2

	#Score V Config:
	#	Max: 16
	p_num_v = 0
	p_sum_v = 0
	op_num_v = 0
	op_sum_v = 0
	for c in p_col_num:
		if(c>=2):
			p_num_v+=1
			p_sum_v+=c
	for c in op_col_num:
		if(c>=2):
			op_num_v+=1
			op_sum_v+=c
	d_v_score = 0
	o_v_score = 0
	if(p_num_v > 0):
		d_v_score = d_rat*int(p_sum_v/p_num_v)
	if(op_num_v > 0):
		o_v_score = o_rat*int(op_sum_v/op_num_v)
	score += (d_v_score)*2

	#Mobility:
	#	Max: 15	
	score += (o_rat*p_mob-d_rat*op_mob)*5

	score /= math.sqrt(o_rat**2+d_rat**2)

	return score

def eval_fn_off(state,p_color):
	return eval_fn(state,p_color,5,1)
	

def eval_fn_def(state,p_color):
	return eval_fn(state,p_color,1,5)


def playBreakthru(eval_white,eval_black,solv_white,solv_black,depth=3):
	curState = BoardState()
	gamestates = [curState]
	turn = 0
	num_moves = 1
	while(curState.getWinner()<0):
		nextState = None
		print 'Move: '+str(turn)+'\tTurn: '+str(num_moves)
		if(turn == 0):
			nextState = solv_white(curState,eval_white,0,0,depth)
			turn = 1
		elif(turn == 1):
			nextState = solv_black(curState,eval_black,1,0,depth)
			turn = 0
		curState = nextState
		gamestates +=[curState]
		num_moves+=1
	num_moves-=1
	return gamestates

def minimax(curState,eval_fn,p_color,curDepth,maxDepth):
	if(curDepth==maxDepth or curState.getWinner()>=0):
		eval_val = eval_fn(curState,p_color)
		curState.setEvalScore(eval_val)
		return curState
	else:
		#if curDepth is even -> MAX else
		#						MIN
		n_color = p_color
		num_exp = 0
		if(curDepth%2 == 1):		#if curDepth is odd
			n_color = 0				#	switch moving color
			if(p_color == 0):
				n_color = 1

		best_val = -1000
		if(curDepth%2==1):
			best_val = 1000
		best_state = None

		pieces = curState.getPieces(n_color)
		for p in pieces:
			moves = curState.getValidMoves(n_color,p)
			for i in moves:
				nextState = curState.copy()
				nextState.makeMove(n_color,p,i)
				tState = minimax(nextState,eval_fn,p_color,curDepth+1,maxDepth)
				num_exp+=tState.getNodeExp()
				if(curDepth%2==0):
					if(tState.getEvalScore()>best_val):
						best_state = tState.copy()
						best_val = best_state.getEvalScore()
				else:
					if(tState.getEvalScore()<best_val):
						best_state = tState.copy()
						best_val = best_state.getEvalScore()
		if(curDepth == 0):
			best_state.setNodeExp(num_exp)
			return best_state
		curState.setNodeExp(num_exp)
		curState.setEvalScore(best_val)
		return curState

def alphabeta(curState,eval_fn,p_color,curDepth,maxDepth):
	return maxvalue(curState,-1000,1000,eval_fn,p_color,curDepth,maxDepth)

def maxvalue(curState,alpha,beta,eval_fn,p_color,curDepth,maxDepth):
	if(curDepth==maxDepth or curState.getWinner()>=0):
		eval_val = eval_fn(curState,p_color)
		curState.setEvalScore(eval_val)
		return curState
	else:
		#if curDepth is even -> MAX else
		#						MIN
		n_color = p_color
		num_exp = 0
		if(curDepth%2 == 1):		#if curDepth is odd
			n_color = 0				#	switch moving color
			if(p_color == 0):
				n_color = 1

		best_val = -1000
		best_state = None
		pieces = curState.getPieces(n_color)
		pieces.sort()			#Try moving most forward pieces first
		if(n_color == 0):
			pieces.reverse()
		for p in pieces:
			moves = curState.getValidMoves(n_color,p)
			for i in moves:
				nextState = curState.copy()
				nextState.makeMove(n_color,p,i)
				tState = minvalue(nextState,alpha,beta,eval_fn,p_color,curDepth+1,maxDepth)
				num_exp+=tState.getNodeExp()
				if(tState.getEvalScore()>best_val):
					best_state = tState.copy()
					best_val = best_state.getEvalScore()
				if(best_val>=beta):
					if(curDepth == 0):
						best_state.setNodeExp(num_exp)
						return best_state
					curState.setNodeExp(num_exp)
					curState.setEvalScore(best_val)
					return curState
				alpha = max(alpha,best_val)
		
		if(curDepth == 0):
			best_state.setNodeExp(num_exp)
			return best_state
		curState.setNodeExp(num_exp)
		curState.setEvalScore(best_val)
		return curState

def minvalue(curState,alpha,beta,eval_fn,p_color,curDepth,maxDepth):
	if(curDepth==maxDepth or curState.getWinner()>=0):
		eval_val = eval_fn(curState,p_color)
		curState.setEvalScore(eval_val)
		return curState
	else:
		#if curDepth is even -> MAX else
		#						MIN
		n_color = p_color
		num_exp = 0
		if(curDepth%2 == 1):		#if curDepth is odd
			n_color = 0				#	switch moving color
			if(p_color == 0):
				n_color = 1

		best_val = 1000
		best_state = None
		pieces = curState.getPieces(n_color)
		pieces.sort()			#Try moving most forward pieces first
		if(n_color == 0):
			pieces.reverse()
		for p in pieces:
			moves = curState.getValidMoves(n_color,p)
			for i in moves:
				nextState = curState.copy()
				nextState.makeMove(n_color,p,i)
				tState = maxvalue(nextState,alpha,beta,eval_fn,p_color,curDepth+1,maxDepth)
				num_exp+=tState.getNodeExp()
				if(tState.getEvalScore()<best_val):
					best_state = tState.copy()
					best_val = best_state.getEvalScore()
				if(best_val<=alpha):
					if(curDepth == 0):
						best_state.setNodeExp(num_exp)
						return best_state
					curState.setNodeExp(num_exp)
					curState.setEvalScore(best_val)
					return curState
				beta = min(beta,best_val)
		
		if(curDepth == 0):
			best_state.setNodeExp(num_exp)
			return best_state
		curState.setNodeExp(num_exp)
		curState.setEvalScore(best_val)
		return curState

def playerPlay(curState,eval_fn,p_color,curDepth,maxDepth):
	pieces = curState.getPieces(p_color)
	pieces.sort()
	print '\n################\n'
	curState.display()
	print 'Pieces Available: \n'
	p_str = ''
	for p in pieces:
		p_str+=str(p)+' '
	print p_str
	c_pos = int(input('Enter Location of Piece to Move: '))
	if(len(curState.getValidMoves(p_color,c_pos))>0):
		t_pos = -1
		while(t_pos not in curState.getValidMoves(p_color,c_pos)):
			p_str = ''
			for p in curState.getValidMoves(p_color,c_pos):
				p_str+=str(p)+' ' 
			print 'Valid Move Locations: \n'+p_str
			t_pos = int(input('Enter Location to Move Piece To: '))
		curState.makeMove(p_color,c_pos,t_pos)
		print '\n################\n'
		return curState
	else:
		print 'Invalid Piece: Cannot move or does not exist, pick another...\n'
		return playerPlay(curState,None,p_color,0,0)

game = []
option = 0
depth = 3
if(len(sys.argv)>1):
	option = int(sys.argv[1])
if(len(sys.argv)>2):
	depth = int(sys.argv[2])

if(option not in range(20)):
	option = 0
if(depth<=0):
	depth = 3
time_diff = 0

time_diff = time.time()
if(option == 0):
	game = playBreakthru(eval_fn_off,eval_fn_def,minimax,minimax,depth)
elif(option == 1):
	game = playBreakthru(eval_fn_def,eval_fn_off,minimax,minimax,depth)
elif(option == 2):
	game = playBreakthru(eval_fn_off,eval_fn_off,minimax,minimax,depth)
elif(option == 3):
	game = playBreakthru(eval_fn_def,eval_fn_def,minimax,minimax,depth)

elif(option == 4):
	game = playBreakthru(eval_fn_off,eval_fn_def,alphabeta,alphabeta,depth)
elif(option == 5):
	game = playBreakthru(eval_fn_def,eval_fn_off,alphabeta,alphabeta,depth)
elif(option == 6):
	game = playBreakthru(eval_fn_off,eval_fn_off,alphabeta,alphabeta,depth)
elif(option == 7):
	game = playBreakthru(eval_fn_def,eval_fn_def,alphabeta,alphabeta,depth)

elif(option == 8):
	game = playBreakthru(eval_fn_off,eval_fn_def,minimax,alphabeta,depth)
elif(option == 9):
	game = playBreakthru(eval_fn_def,eval_fn_off,minimax,alphabeta,depth)
elif(option == 10):
	game = playBreakthru(eval_fn_off,eval_fn_off,minimax,alphabeta,depth)
elif(option == 11):
	game = playBreakthru(eval_fn_def,eval_fn_def,minimax,alphabeta,depth)

elif(option == 12):
	game = playBreakthru(eval_fn_off,eval_fn_def,alphabeta,minimax,depth)
elif(option == 13):
	game = playBreakthru(eval_fn_def,eval_fn_off,alphabeta,minimax,depth)
elif(option == 14):
	game = playBreakthru(eval_fn_off,eval_fn_off,alphabeta,minimax,depth)
elif(option == 15):
	game = playBreakthru(eval_fn_def,eval_fn_def,alphabeta,minimax,depth)

elif(option == 16):
	game = playBreakthru(eval_fn_def,eval_fn_def,playerPlay,alphabeta,depth)
elif(option == 17):
	game = playBreakthru(eval_fn_def,eval_fn_off,playerPlay,alphabeta,depth)
elif(option == 18):
	game = playBreakthru(eval_fn_def,eval_fn_def,alphabeta,playerPlay,depth)
elif(option == 19):
	game = playBreakthru(eval_fn_off,eval_fn_def,alphabeta,playerPlay,depth)

time_diff = time.time()-time_diff

avg_time = time_diff/(len(game)-1)
print time_diff

turn_num = 0
white_states = 0
black_states = 0
str_out = ''
print '\n################\n'
for g in game:
	turn_num+=1
	print '----Turn #: '+str(turn_num)+'----\n'
	g.display()
	print 'Winner: '+str(g.getWinner())
	print '-White Captures: '+str(g.getCaptures(0))
	print '-Black Captures: '+str(g.getCaptures(1))
	print '-Nodes Expanded: '+str(g.getNodeExp())
	print '\n################\n'
	if(turn_num%2==1):
		black_states+=g.getNodeExp()
	else:
		white_states+=g.getNodeExp()

g = game[len(game)-1]
str_out += '----Turn #: '+str(turn_num)+'----\n\n'
str_out += g.display()+'\n'
str_out += 'Winner: '+str(g.getWinner())+'\n'
str_out += '-White Captures: '+str(g.getCaptures(0))+'\n'
str_out += '-Black Captures: '+str(g.getCaptures(1))+'\n'
str_out += '\n################\n'

print "White States Expanded  : "+str(white_states)
print "Black States Expanded  : "+str(black_states)
print "Nodes Expanded per Turn: "+str((black_states+white_states)/len(game))
print 'Avg. Turn Time         : '+str(avg_time)+'[s]'

str_out += 'White States Expanded  : '+str(white_states)+'\n'
str_out += 'Black States Expanded  : '+str(black_states)+'\n'
str_out += 'Nodes Expanded per Turn: '+str((black_states+white_states)/(len(game)-1))+'\n'
str_out += 'Avg. Turn Time         : '+str(avg_time)+'[s]\n'

fo = open('breakthru3_'+str(option)+'_'+str(depth)+'.txt','w')
fo.write(str_out)
fo.close()
