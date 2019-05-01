#!/usr/bin/python

def readBank(filename):

	words = [line.rstrip('\n') for line in open(filename, 'r')]
	words = [word.upper() for word in words]
	words.sort(lambda x, y: cmp(len(x), len(y)))
	words.reverse()
	return words