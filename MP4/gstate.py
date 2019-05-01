#!/usr/bin/python

class GState(object):

	def __init__(self,ball_x,ball_y,ball_x_vel,ball_y_vel,paddle_y):
		self.Q = [0,0,0]	#[-1,0,1]
		self.N = [0,0,0]	#[-1,0,1]
		self.x_ball = ball_x
		self.y_ball = ball_y
		self.vel_x_ball = ball_x_vel
		self.vel_y_ball = ball_y_vel
		self.y_pad = paddle_y

	def copy(self):
		ret = GState(self.x_ball,self.y_ball,self.vel_x_ball,self.vel_y_ball,self.y_pad)
		ret.Q = self.Q[:]
		ret.N = self.N[:]
		return ret

	def getQ(self,a):		#a is action of paddle-->[-1,0,1]
		return self.Q[a+1]

	def getN(self,a):
		return self.N[a+1]

	def setQ(self,Qnew,a):
		self.Q[a+1] = Qnew

	def incrN(self,a):
		self.N[a+1]+=1

	def isTerminal(self, disc_div):
		return self.x_ball >= disc_div

	def reset(self):
		self.Q = [0,0,0]
		self.N = [0,0,0]