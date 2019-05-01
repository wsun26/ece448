#!/usr/bin/python

class State(object):
	
	def __init__(self,loc,goals):
		self.location = loc
		self.goals = goals[:]
		self.parent = None
		self.cost = 0
		self.f_n = 0
		self.num_goals = sum(self.goals)
		
	def __hash__(self):
		val = 0
		str_g=''.join(str(e) for e in self.goals)
		#str_g = self.getNumGoals()
		return hash((self.location,str_g))
		
	def __eq__(self,other):
		return (self.location,self.goals)==(other.location,other.goals)
		#return (self.location,self.getNumGoals())==(other.location,other.getNumGoals())

	def __cmp__(self,other):
		return cmp(self.f_n,other.f_n)

	def __ne__(self,other):
		return not(self==other)
		
	def __repr__(self):
		return str(self)
		
	def __str__(self):
		return "Loc: "+str(self.location)+":::"+''.join(str(e) for e in self.goals)
		
	def getLoc(self):
		return self.location
		
	def getGoals(self):
		return self.goals
		
	def getParent(self):
		return self.parent
		
	def getCost(self):
		return self.cost

	def complete(self):
		return (not 0 in self.goals)
		
	def setParent(self,parent):
		self.parent = parent
		
	def setCost(self, cost):
		self.cost = cost

	def setGoal(self, index, val):
		if(self.goals[index]==0 and val == 1):
			self.num_goals+=1
		elif(self.goals[index]==1 and val == 0):
			self.num_goals-=1
		self.goals[index] = val

	def setGoals(self,goals):
		self.goals = goals[:]
		self.num_goals = sum(goals)

	def setFunc(self,f_n):
		self.f_n = f_n

	def getNumGoals(self):
		return self.num_goals
		
	def getCoord(self,width):
		return (self.location%width,self.location/width)

	def getFunc(self):
		return self.f_n
