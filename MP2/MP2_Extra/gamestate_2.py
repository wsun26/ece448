#!/usr/bin/python

class BoardState(object):
	def __init__(self):
		self.p_white = [i for i in range(16)]
		self.p_black = [j for j in range(48,64)]
		self.white_cap = 0
		self.black_cap = 0
		self.num_exp = 1
		self.eval_score = 0
		self.winner = -1		#0 white, 1 black

	def copy(self):
		ret = BoardState()
		ret.p_white = self.p_white[:]
		ret.p_black = self.p_black[:]
		ret.white_cap = self.white_cap
		ret.black_cap = self.black_cap
		ret.eval_score = self.eval_score
		ret.winner = self.winner
		return ret

	def updateWinner(self):
		'''	White Wins: in 56+
			Black Wins: in 7-'''
		if(self.winner>=0):
			return
		if(len(self.p_black)<3):
			self.winner = 0
			return
		if(len(self.p_white)<3):
			self.winner = 1
			return

		self.p_white.sort()
		w_goal = 0
		for w in self.p_white[len(self.p_white)-3:]:
			if(w >= 56):
				w_goal+=1
		if(w_goal==3):
			self.winner = 0
			return

		self.p_black.sort()
		b_goal = 0
		for b in self.p_black[len(self.p_black)-3:]:
			if(b < 8):
				b_goal+=1
		if(b_goal==3):
			self.winner = 1

	def makeMove(self,color,pos_from,pos_to):
		'''Color: 0 = White, 1 = Black'''
		if(color == 0):
			#Assume move has been verified
			self.p_white[self.p_white.index(pos_from)] = pos_to
			if(pos_to in self.p_black):
				self.p_black.remove(pos_to)
				self.white_cap+=1
		elif(color == 1):
			#Assume move has been verified
			self.p_black[self.p_black.index(pos_from)] = pos_to
			if(pos_to in self.p_white):
				self.p_white.remove(pos_to)
				self.black_cap+=1
		self.updateWinner()

	def getValidMoves(self,color,pos):
		if(color == 0):
			if(pos not in self.p_white or pos >= 56):
				return []
			else:
				moves = []
				#Check Down Left
				if(pos%8!=0 and pos+7 not in self.p_white):
					moves += [pos+7]
				#Check Down
				if(pos+8 not in self.p_black and pos+8 not in self.p_white):
					moves += [pos+8]
				#Check Down Right
				if(pos%8!=7 and pos+9 not in self.p_white):
					moves += [pos+9]
				return moves
		elif(color == 1):
			if(pos not in self.p_black or pos < 8):
				return []
			else:
				moves = []
				#Check Up Left
				if(pos%8!=0 and pos-9 not in self.p_black):
					moves += [pos-9]
				#Check Down
				if(pos-8 not in self.p_white and pos-8 not in self.p_black):
					moves += [pos-8]
				#Check Up Right
				if(pos%8!=7 and pos-7 not in self.p_black):
					moves += [pos-7]
				return moves

	def setEvalScore(self,eval_val):
		self.eval_score = eval_val

	def setNodeExp(self,val):
		self.num_exp = val

	def getNodeExp(self):
		return self.num_exp

	def getPieces(self,color):
		if(color == 0):
			return self.p_white
		elif(color == 1):
			return self.p_black
		return []

	def getEvalScore(self):
		return self.eval_score

	def getWinner(self):
		return self.winner

	def getCaptures(self,color):
		if(color == 0):
			return self.white_cap
		elif(color == 1):
			return self.black_cap
		return 0

	def display(self):
		txt = ''
		for i in range(64):
			if(i in self.p_black):
				txt += 'B'
			elif(i in self.p_white):
				txt += 'W'
			else:
				txt += '-'
			if(i%8==7):
				txt+='\n'
		print txt
		return txt