#!/usr/bin/python
from searcher import Searcher
from mstate import State
from mazeio import *
import sys
import time
from math import sqrt


def DFS(frontier,goals,width,cur_state): 
	return [cur_state]+frontier
	
def BFS(frontier,goals,width,cur_state):
	return frontier+[cur_state]
	
def Greedy(frontier,goals,width,cur_state):
	f_n_new = man(goals,width,cur_state)
	cur_state.setFunc(f_n_new)
	i=0
	while(i<len(frontier) and f_n_new>=frontier[i].getFunc()):
		if(f_n_new == frontier[i].getFunc() and cur_state.getNumGoals()>frontier[i].getNumGoals()):
			frontier.insert(i,cur_state)
			return frontier
		i+=1
	if(i==len(frontier)):
		return frontier+[cur_state]
	frontier.insert(i,cur_state)
	return frontier

def AStar(frontier,goals,width,cur_state):
	f_n_new = f_n(goals,width,cur_state)
	cur_state.setFunc(f_n_new)
	i=0
	while(i<len(frontier) and f_n_new>=frontier[i].getFunc()):
		if(f_n_new == frontier[i].getFunc() and cur_state.getNumGoals()>frontier[i].getNumGoals()):
			frontier.insert(i,cur_state)
			return frontier
		i+=1
	if(i==len(frontier)):
		return frontier+[cur_state]
	frontier.insert(i,cur_state)
	return frontier

def SubOpt(frontier,goals,width,cur_state):
	f_n_new = sub(goals,width,cur_state)
	cur_state.setFunc(f_n_new)
	i=0
	while(i<len(frontier) and f_n_new>=frontier[i].getFunc()):
		if(f_n_new == frontier[i].getFunc() and cur_state.getNumGoals()>frontier[i].getNumGoals()):
			frontier.insert(i,cur_state)
			return frontier
		i+=1
	if(i==len(frontier)):
		return frontier+[cur_state]
	frontier.insert(i,cur_state)
	return frontier

def f_n(goals,width,state):
	global h1, h2, h3
	s_x, s_y = state.getCoord(width)
	man_max = 0
	man_sum = 0
	man_min = width**2
	i = 0
	goals_left = []
	while i < len(goals):
		if(state.getGoals()[i]==0):
			g_x = goals[i]%width
			g_y = goals[i]/width 
			f_n = 0
			h_n = 0
			man_dist = abs(g_x-s_x) + abs(g_y-s_y)
			man_sum += man_dist
			man_max=max(man_dist, man_max)
			man_min=min(man_dist, man_min)
			goals_left+=[goals[i]]
			
		i+=1
	goal1 = -1
	goal2 = -1
	g_max = 0
	
	g_min = [-1 for x in goals_left]
	g_min_g = [x for x in range(len(goals_left))]
	i = 0
	while i < len(goals_left):
		g1 = goals_left[i]
		for g2 in goals_left:
			g1_x = g1%width
			g1_y = g1/width
			g2_x = g2%width
			g2_y = g2/width
			g_man = abs(g1_x-g2_x) + abs(g1_y-g2_y)
			if(g_man>g_max):
				g_max = g_man
				goal1 = g1
				goal2 = g2
			if(g1!=g2 and (g_min[i]<0 or (g_man<g_min[i] and g_min_g[goals_left.index(g2)]!=g1))):
				g_min[i]=g_man
				g_min_g[i] = g2
		i+=1
	g_mins = sum(g_min)
	g_mins2 = 0

	
	dist_to_far = 0
	if(goal1>=0 and goal2>=0):
		dist1 = abs(s_x-g1%width) + abs(s_y-g1/width)
		dist2 = abs(s_x-g2%width) + abs(s_y-g2/width)
		dist_to_far=min(dist1,dist2)

	num_left = len(goals)-state.getNumGoals()
	h_n = max(num_left+man_min,g_max+dist_to_far,man_min+g_mins)
	g_n = state.getCost()

	return h_n+g_n

def man(goals,width,state):
	s_x,s_y = state.getCoord(width)
	man_max = 0
	i = 0
	while i < len(goals):
		if(state.getGoals()[i]==0):
			g = goals[i]
			g_x = g%width
			g_y = g/width
			man_max = max(abs(g_x-s_x)+abs(g_y-s_y),man_max)
		i+=1
	return man_max

def sub(goals,width,state):
	return f_n(goals,width,state)/(state.getNumGoals()**2+1)
		
	
dfs = Searcher(DFS)
bfs = Searcher(BFS)
greedy = Searcher(Greedy)
a_star = Searcher(AStar)
subopt = Searcher(SubOpt)

file_name = sys.argv[1]
option = int(sys.argv[2])
s = None

if(option==0):
	s=dfs
elif(option==1):
	s=bfs
elif(option==2):
	s=greedy
elif(option==3):
	s=a_star
elif(option==4):
	s=subopt


(state_space,start,goals,width) = ReadMaze(file_name)
strt_t = time.time()
(sol,node_exp,cost) = s.genPath(state_space,start,goals,width)
a_star_t = time.time()-strt_t
print '\nExpanded: '+str(node_exp)+'\nCost: '+str(cost)

DrawMaze(sol,file_name,width)

print 'Time: '+str(a_star_t)