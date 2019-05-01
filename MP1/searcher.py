#!/usr/bin/python
from mstate import State
from mazeio import ReadMaze
import sys

class Searcher(object):

	def __init__(self, strategy):	#input is object map
		self.strategy = strategy;	#some list/array/matix object
		
	def genPath(self, maze, start, goals, width):
		node_exp = 1
		cost = -1
		path = []
		if(not maze.has_key(start)):
			print "Error: Start is not a valid location"
			return ([],-1,-1)
		blank_goal = [0 for x in goals]
		cur_state = State(start,blank_goal)
		frontier = [cur_state]
		f_map = {}
		f_map[cur_state] = True
		explored = {}
		max_goals = 0
		while(len(frontier)>0):
			cur_state = frontier[0]
			frontier = frontier[1:]
			del f_map[cur_state]

			if(cur_state.getLoc() in goals):
				cur_state.setGoal(goals.index(cur_state.getLoc()),1)

			if(cur_state.complete()):
				while(cur_state):
					path=[cur_state.getLoc()]+path
					cur_state = cur_state.getParent()
					cost+=1

				return (path,node_exp,cost)

			explored[cur_state] = True

			node_exp+=1

			for st in maze[cur_state.getLoc()]:
				state = State(st,cur_state.getGoals())
				if(state not in explored or not explored[state]):
					if(state in f_map):
						f_state = frontier[frontier.index(state)]
						if(f_state.getCost()>cur_state.getCost()+1):
							frontier.remove(f_state)
							f_state.setCost(cur_state.getCost()+1)
							f_state.setParent(cur_state)
							frontier = self.strategy(frontier, goals,width,f_state)
					else:
						state.setParent(cur_state)
						state.setCost(cur_state.getCost()+1)
						frontier = self.strategy(frontier,goals,width,state)
						f_map[state] = True


			if(cur_state.getNumGoals()>max_goals):
				max_goals = cur_state.getNumGoals()

			if(node_exp%100==0):
				print node_exp/100,":",max_goals,"/",len(goals),"F_len:",len(frontier)
				pass
		
		print "Could not find the solution"
		return ([],-1,-1)