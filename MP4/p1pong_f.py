#!/usr/bin/python
from gstate import GState
from ball import Ball
from paddle import Paddle
import random as r
from graphics import *
import time

disc_div = 12
Ne = 64# 128 #72
gamma = .72#0.373 (2/0.3)^gamma = 0.1
alpha_fac = float(385)#771)	#434

#Let Navg = game_ct*(2/0.3)*10/2/(12*12*12*2*3+1)
#Ne = Navg/4 (explore 1/3 of time)
#alpha_fac = Navg/9 (last learning should be weighted 1/10)

'''Good Result 1: 9.08 avg
	Ne = 100
	gamma = 0.75
	alpha_fac = 1000
'''

windows_size = 640
refresh_rate = 1.0/30.0

pos_actions = [-1,0,1]
pos_vel_x = [-1,-0.5,0.5,1]
pos_vel_y = [-1,0,1]

def trainGame(game_ct = 100000):
	ct = 0
	bounces = 0
	max_bounces = 0
	ball = Ball()
	paddle = Paddle()
	pos_actions = [-1,0,1]

	state_space = [[[[[None for x in range(disc_div)] for y in pos_vel_y] for z in pos_vel_x] for w in range(disc_div)] for v in range(disc_div)]
	fail_state = GState(disc_div,0,0,0,0)	#Ball x > 1 aka failure 
	for x in range(disc_div):
		for y in range(disc_div):
			for velx in pos_vel_x:
				for vely in pos_vel_y:
					for p_y in range(disc_div):
						state_space[x][y][pos_vel_x.index(velx)][pos_vel_y.index(vely)][p_y] = GState(x,y,velx,vely,p_y)
	print game_ct
	prev_state = None
	prev_action = None
	prev_R = None
	while(ct < game_ct):
		cur_state = None
		disc_vals = DiscretizeCurrentState(ball,paddle)
		if(disc_vals[0]>=disc_div):
			cur_state = fail_state
		else:
			cur_state = state_space[disc_vals[0]][disc_vals[1]][disc_vals[2]][disc_vals[3]][disc_vals[4]]
		#cur_state = next_state
		if(prev_state!=None):
			prev_state.incrN(prev_action)

			newQ = prev_state.getQ(prev_action)
			newQ = newQ + (alpha_fac/(alpha_fac+prev_state.getN(prev_action)))*(prev_R+gamma*max([cur_state.getQ(ap) for ap in pos_actions])-newQ)
			prev_state.setQ(newQ,prev_action)
			#print newQ
		if(cur_state.isTerminal(disc_div)):
			prev_state = None
			prev_action = None
			prev_R = None

			ball.reset()
			paddle.reset()
			ct+=1
			if(bounces>max_bounces):
				max_bounces = bounces
			bounces = 0
		else:
			action_values = [Fn(cur_state.getQ(a),cur_state.getN(a)) for a in pos_actions]		#[value for action -1, value for action 0, value for action 1]
			max_a = max(action_values)
			max_action_choices = []
			for a in pos_actions:
				if(action_values[a+1] == max_a):
					max_action_choices.append(a)

			r.shuffle(max_action_choices)

			prev_action = max_action_choices[0]

			paddle.movePaddle(prev_action)
			prev_R = ball.updatePos(paddle.getY(),paddle.getHeight())
			prev_state = cur_state

			if(prev_R>0):
				bounces+=1

			if(float(ct)*100/game_ct == ct*100/game_ct and ct*100/game_ct>0):
				print str(ct*100/game_ct)+"%"
		#drawGame(ball,paddle,win,cir,pad)
	
	ret = (max_bounces,state_space,fail_state)
	return ret

def testGame(state_space, fail_state, test_ct = 1000):
	win = GraphWin("1P Pong",windows_size,windows_size)

	ball = Ball()
	paddle = Paddle()
	cir,pad = setUpDrawGame(ball,paddle,win)

	ct = 0
	total_bounces = 0
	prev_state = None
	prev_action = None
	prev_R = None
	while(ct < test_ct):
		cur_state = None
		disc_vals = DiscretizeCurrentState(ball,paddle)
		if(disc_vals[0]>=disc_div):
			cur_state = fail_state
		else:
			cur_state = state_space[disc_vals[0]][disc_vals[1]][disc_vals[2]][disc_vals[3]][disc_vals[4]]
		#cur_state = next_state
		if(cur_state.isTerminal(disc_div)):
			prev_state = None
			prev_action = None
			prev_R = None

			ball.reset()
			paddle.reset()
			ct+=1
		else:
			action_values = [cur_state.getQ(a) for a in pos_actions]		#[value for action -1, value for action 0, value for action 1]
			max_a = max(action_values)
			max_action_choices = []
			for a in pos_actions:
				if(action_values[a+1] == max_a):
					max_action_choices.append(a)

			r.shuffle(max_action_choices)

			prev_action = max_action_choices[0]

			paddle.movePaddle(prev_action)
			prev_R = ball.updatePos(paddle.getY(),paddle.getHeight())
			prev_state = cur_state

			if(prev_R>0):
				total_bounces+=1
		if(test_ct-ct<=1):
			drawGame(ball,paddle,win,cir,pad)

	win.getMouse()
	win.close()
	ret = float(total_bounces)/test_ct
	return ret

def Fn(u,n):
	if(n<Ne):
		return 100
	else:
		return u


def DiscretizeCurrentState(ball,paddle):
	ball_x,ball_y = ball.getPos()

	if(ball_x>1):
		return (disc_div,0,0,0,0)

	if(ball_x == 1):
		ball_x = disc_div-1
	else:
		ball_x = (int)(ball_x * disc_div)
	if(ball_y == 1):
		ball_y = disc_div-1
	else:
		ball_y = (int)(ball_y * disc_div)

	vel_x,vel_y = ball.getVel()
	vel_x_o = vel_x
	if(vel_x>0):
		vel_x = 1
	else:
		vel_x = -1

	if(abs(vel_x_o)<0.050):
		vel_x*=0.5

	if(vel_y>0.015):
		vel_y = 1
	elif(vel_y<-0.015):
		vel_y = -1
	else:
		vel_y = 0

	paddle_y = paddle.getY()
	if(paddle_y == 1-paddle.getHeight()):
		paddle_y = disc_div-1
	else:
		paddle_y = (int)(disc_div*paddle_y/(1-paddle.getHeight()))

	return (ball_x,ball_y,pos_vel_x.index(vel_x), pos_vel_y.index(vel_y), paddle_y)

def saveStates(state_space,fail_state, avg):
	f_name = str(avg)+'_'+str(Ne)+'_'+str(gamma)+'_'+str(alpha_fac)
	f_name = f_name.replace('.','-')
	f_name+='.txt'
	f_out = open(f_name,'w')
	str_out = ''
	pos_actions = [-1,0,1]
	for x in range(disc_div):
		for y in range(disc_div):
			for velx in pos_vel_x:
				for vely in pos_vel_y:
					for p_y in range(disc_div):
						cur_state = state_space[x][y][pos_vel_x.index(velx)][pos_vel_y.index(vely)][p_y]
						for a in pos_actions:
							str_out+=str(cur_state.getQ(a))+' '
						str_out = str_out[:-1]
						str_out += '\n'
	for a in pos_actions:
		str_out+=str(fail_state.getQ(a))+' '
	str_out = str_out[:-1]
	f_out.write(str_out)
	f_out.close()

def setUpDrawGame(ball,paddle,win):
	left = Line(Point(0,0),Point(0,windows_size))
	left.setWidth(6)
	left.draw(win)


	pad = Line(Point(1*windows_size,paddle.getY()*windows_size),Point(windows_size,paddle.getY()*windows_size+paddle.getHeight()*windows_size))
	pad.setWidth(10)
	pad.draw(win)

	t = 0
	ball_x, ball_y = ball.getPos()
	cir = Circle(Point(ball_x*windows_size,ball_y*windows_size),windows_size/160)
	cir.draw(win)
	cir.setFill("black")
	return cir,pad
	#win.close()

def drawGame(ball,paddle,win,cir,pad):
	ball_x, ball_y = ball.getPos()
	c_x, c_y = (cir.getCenter().getX(),cir.getCenter().getY())
	cir.move(ball_x*windows_size-c_x,ball_y*windows_size-c_y)
	p_y = pad.getP1().getY()
	pad.move(0,paddle.getY()*windows_size-p_y)
	time.sleep(refresh_rate)

t = time.time()
m_b,learned_states,fail_state = trainGame(150000)
time_run = time.time()-t;
t_b = testGame(learned_states,fail_state,2000)
print "Max Bounces: "+str(m_b)+"\nAverage Bounces/Game: "+str(t_b)
print "It took: "+str(time_run/60.0)+" min to complete"
saveStates(learned_states,fail_state,t_b)
#drawGame(None,None)
