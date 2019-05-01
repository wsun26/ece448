#!/usr/bin/python

class Paddle(object):

	def __init__(self):
		self.x = 1
		self.height = 0.2
		self.y = 0.5-self.height/2

	def getY(self):
		return self.y

	def getHeight(self):
		return self.height

	def movePaddle(self,dir):	#+1: Down; 0: Nowhere; -1: Up
		self.y+=dir*0.04
		if(self.y+self.height>1):
			self.y = 1-self.height
		elif(self.y<0):
			self.y = 0

	def reset(self):
		self.__init__()