import sys
sys.setrecursionlimit(10000)

from pyPL import *
from helper import *

class State(Enum):
	W = 1
	P = 2
	S = 3
	B = 4
	OK = 5
	PW = 6
	PP = 7

class Agent:
	def __init__(self, w, h):
		self.size = w, h
		self.kb = initRules(w,h)	# knowledge base 
		self.score = 0 				# score
		self.p = 1, 1				# position

		self.moveCnt = 150              # allowance for move cnt
		self.worldState = {} 
		self.unvisited = set()
		self.ok = set()
		for x in range (1, w+1):
			for y in range(1, h+1):
				self.worldState[(x,y)] = set()
				self.unvisited.add((x,y))
		self.plan = []
		self.adjList = {}

	def pCNF(cnf):
		for clause in kb:
			print(str([str(u) for u in list(clause)]))

	def updateKB(self, world):
		percepts = world.perceptsAt(self.p)
		pSentences = AtomicSentence(True, "True")
		# sentences for those are in current percepts	
		for p in percepts:
			if p != "G" and p != "A":
				pSentences = pSentences.cAnd(makePerceptSentence(p, self.p[0], self.p[1]))
			self.worldState[self.p].add(p)
			self.ok.add(self.p)
		# sentences for those are not in current percepts	
		notPercepts = [p for p in world.percepts if p not in percepts]
		for p in notPercepts:
			pSentences = pSentences.cAnd(~makePerceptSentence(p, self.p[0], self.p[1]))
		cnf = pSentences.cnf()
		# for clause in cnf:
		# 	print(str([str(u) for u in list(clause)]))
		self.kb.extend(cnf)

	def makePlan(self):
		if "G" in self.worldState[self.p]:
			self.plan.append(Act.GRAB_GOLD) 
		if len(self.plan) == 0:
			# visits the closest safe unvisited square
			goals = set([u for u in self.unvisited if u in self.ok])
			if len(goals) > 0:
				adjList = {}
				for u in self.ok:
					adjList[u] = []
					neis = neighbors(u[0], u[1], self.size[0], self.size[1])
					for nei in neis:
						if nei in self.ok:
							adjList[u].append(nei)
					print(adjList)
			self.plan.extend(aStarSearch(self.p, adjList, goals))
		# if len(self.plan) == 0:


	def updateWorldState(self):
		neis = neighbors(self.p[0], self.p[1], self.size[0], self.size[1])
		for pos in neis + [self.p]:
			notPitSentence = ~(makePerceptSentence("P", pos[0], pos[1]))
			notPit = resolution(self.kb, notPitSentence)
			notWumpusSentence = ~(makePerceptSentence("W", pos[0], pos[1]))
			notWumpus = resolution(self.kb, notWumpusSentence)
			if notWumpus and notPit:
				self.kb.extend(notWumpusSentence.cnf())
				self.kb.extend(notPitSentence.cnf())
				self.ok.add(pos)
			else:
				if not notPit: 
					# there is a possible pit
					self.worldState[pos].add("PP")
				if not notWumpus:
					# there is a possible wumpus
					self.worldState[pos].add("WP")
		if self.p in self.unvisited: 
			self.unvisited.remove(self.p)

	def planRoute(self, current, goals):
		actions = []
		return actions

	def act(self):
		i = 0 
		perceptsToRemove = {}
		while i < len(self.plan):
			if self.plan[i].value == 1:
				self.move(self.plan[i])
			elif self.plan[i] == Act.GRAB_GOLD:
				perceptsToRemove["G"] = [self.p] 
				self.pickGold()
			i += 1
		return perceptsToRemove

	def do(self, world):
		self.updateKB(world)
		self.updateWorldState()
		self.makePlan()
		return self.act()
	# def moveUp(self):
	# 	self.p[1] += 1 

	# def moveDown(self):
	# 	self.p[1] -= 1

	# def moveLeft(self):
	# 	self.p[0] -= 1 

	# def moveRight(self):
	# 	self.p[0] += 1

	def pickGold(self):
		self.score += Act.GRAB_GOLD.value

	def shootArrow(self):
		self.score += Act.SHOOT_ARROW.value

	def die(self):
		self.score += Act.DIE.value

	def move(self, act):
		if act == Act.UP:
			self.p[1] += 1 
		elif act == Act.DOWN:
			self.p[1] -= 1
		elif act == Act.LEFT:
			self.p[0] -= 1 
		else:
			self.p[0] += 1


		 

