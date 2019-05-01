#!/usr/bin/python
import random as r

class Ball(object):

	def __init__(self):
		self.x = 0.5
		self.y = 0.5
		self.x_vel = 0.03
		self.y_vel = 0.01

	def updatePos(self,y_pad,h_pad):
		self.x += self.x_vel
		self.y += self.y_vel

		if(self.y<0):
			self.bounceTop()
		elif(self.y>1):
			self.bounceBot()

		if(self.x<0):
			self.bounceLeft()

		if(self.x>1):
			m = self.y_vel/self.x_vel
			b = self.y - m*self.x
			y_hit = m*1+b
			if(y_hit>=y_pad and y_hit<=y_pad+h_pad):
				self.bouncePaddle()
				return 1			#Bounced off of paddle
			else:
				return -1			#Out of play
		return 0					#Not out of play	

	def getPos(self):
		return (self.x,self.y)

	def getVel(self):
		return (self.x_vel,self.y_vel)

	def bounceTop(self):
		self.y = -self.y
		self.y_vel = -self.y_vel

	def bounceBot(self):
		self.y = 2-self.y
		self.y_vel = -self.y_vel

	def bounceLeft(self):
		self.x = -self.x
		self.x_vel = -self.x_vel

	def bouncePaddle(self):
		self.x = 2-self.x
		self.x_vel = -self.x_vel+r.uniform(-0.015,0.015)
		self.y_vel = self.y_vel+r.uniform(-0.03,0.03)
		if(abs(self.x_vel)<0.03):
			self.x_vel = 0.03*abs(self.x_vel)/self.x_vel #Keep same direction
		if(abs(self.x_vel)>1):
			self.x_vel = abs(self.x_vel)/self.x_vel #Keep same direction
		if(abs(self.y_vel)>1):
			self.y_vel = abs(self.y_vel)/self.y_vel

	def reset(self):
		self.__init__()