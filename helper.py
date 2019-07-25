import sys
sys.path.append('../')
from pyPL import *
from math import sqrt
from enum import Enum

class Act(Enum) :
	GRAB_GOLD = 100
	SHOOT_ARROW = -100
	DIE = -10000 
	EXIT_CAVE = 0
	STEP = 1

def neighbors(x, y, w, h):
	neis = []
	if x + 1 <= w:
		neis.append((x+1, y))
	if x - 1 >= 1:
		neis.append((x-1, y))
	if y + 1 <= h:
		neis.append((x, y+1))
	if y - 1 >= 1:
		neis.append((x, y-1))
	return neis

def makePerceptSentence(percept, x, y):
	return AtomicSentence(True, percept + str(x)+"_"+str(y))

def initRules(w,h):
	""" Initialize knowledge base from the size of the map 
	and rules of the game Wumpus World:
		feeling a breeze if near a pit
		One room contains a Wumpus that will eat us
		smelling a stench if near the Wumpus

		Notation:
			s<x>_<y>: there's a stench in position (x, y)
			w<x>_<y>: there's a Wumpus in position (x, y)
			b<x>_<y>: there's a breeze in position (x, y)
			p<x>_<y>: there's a pit in position (x, y)

			Example: p1_10: a pit in (1,10)
	"""
	rules = AtomicSentence(True, "True")
	for x in range(1, w+1):
		for y in range(1, h+1):
			wumpus =  makePerceptSentence("W",x,y)
			pit =  makePerceptSentence("P",x,y)
			# rules for ok square 
			rules = rules.cAnd(makePerceptSentence("OK",x,y).cImp((~wumpus).cAnd(~pit)))
			# pit and wumpus can't be at the same position
			rules = rules.cAnd(wumpus.cImp(~pit))
			for x,y in neighbors(x, y, w, h):
				# rules for stench and Wumpus
				stench =  makePerceptSentence("S",x,y)
				rules = rules.cAnd(wumpus.cImp(stench))
				# rules for breeze and pit
				breeze =  makePerceptSentence("B",x,y)
				rules = rules.cAnd(pit.cImp(breeze))
	cnf = rules.cnf()	
	return KnowledgeBase(cnf)

def percepts(problem, kb):
	""" Return all perceptions at each position in the map 
	corresponding the problem 
	"""
	return None

def readProblem(file):
	problem = {}
	f = open(file, "r")
	for line in f:
		l = line.rstrip().split(",")
		key = []
		for i in range(len(l)):
			if i > 1:
				key += l[i]
		problem[(int(l[0]), int(l[1]))] = set(key)
	return problem	

def pCNF(cnf):
	for clause in cnf:
		print(str([str(u) for u in list(clause)]))

def distance(p0, p1):
	return sqrt( (p0[0]-p1[0])*(p0[0]-p1[0]) + (p0[1]-p1[1])*(p0[1]-p1[1]) )
