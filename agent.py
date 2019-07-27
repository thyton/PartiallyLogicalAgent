import sys
sys.setrecursionlimit(10000)

from pyPL import *
from helper import *
from a_search import aStarSearch
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
		print(self.kb)
	def pCNF(self, kb):
		for clause in kb:
			print(str([str(u) for u in list(clause)]))

	def updateKB(self, world):
		# mark this place as safe
		self.ok.add(self.p)

		percepts = world.perceptsAt(self.p)
		pSentences = AtomicSentence(True, "True")
		# sentences for those are in current percepts	
		for p in percepts:
			if p != "G" and p != "A":
				pSentences = pSentences.cAnd(makePerceptSentence(p, self.p[0], self.p[1]))
				self.worldState[self.p].add(p)

		# sentences for those are not in current percepts	
		notPercepts = [p for p in world.percepts if p not in percepts]
		for p in notPercepts:
			neis = neighbors(self.p[0], self.p[1], self.size[0], self.size[1])
			if p == "B":
				[self.worldState[nei].remove("PP") for nei in neis if "PP" in self.worldState[nei]] 
			if p == "S":
				[self.worldState[nei].remove("PW") for nei in neis if "PW" in self.worldState[nei]] 
			pSentences = pSentences.cAnd(~makePerceptSentence(p, self.p[0], self.p[1]))
		cnf = pSentences.cnf()
		# for clause in cnf:
		# 	print(str([str(u) for u in list(clause)]))
		self.kb.extend(cnf)

	def constructGraph(self, allowed):
		adjList = {}
		for u in allowed:
			adjList[u] = []
			neis = neighbors(u[0], u[1], self.size[0], self.size[1])
			for nei in neis:
				if nei in allowed:
					adjList[u].append(nei)
		return adjList

	def makePlan(self, world):
		if "G" in world.perceptsAt(self.p):
			self.plan.append(Act.GRAB_GOLD) 

		if len(self.plan) == 0:
			# visits the closest safe unvisited square
			goals = set([u for u in self.unvisited if u in self.ok])
			print("safe unvisited from self.p", self.p , goals)
			if len(goals) > 0:
				adjList = self.constructGraph(self.ok)
				result = aStarSearch(self.p, goals, adjList)
				self.p = result['steps'][-1]
				self.plan.extend(result['plan'])

		if len(self.plan) == 0:
			# go where there is a possible wumpus but not a possible pit
			goals = set([u for u in self.unvisited if "PW" in self.worldState[u]])
			if len(goals) > 0:
				allowed = copy.deepcopy(self.ok).union(goals)
				adjList = self.constructGraph(allowed)
				result = aStarSearch(self.p, goals, adjList)
				self.p = result['steps'][-1]
				self.plan.extend(result['plan'])
				self.plan.append(Act.SHOOT_ARROW)
				
				# remove the possible wumpus tag from the shoot place
				self.worldState[self.p].remove("PW")

				# update the knowledge base of current place
				notWumpus = ~makePerceptSentence("W", self.p[0], self.p[1])
				self.kb.extend(notWumpus.cnf())

		if len(self.plan) == 0:		
			# go where it is not safe, taking risk
			for u in self.unvisited:
				goals = set()
				notOKSentence = ~(makePerceptSentence("OK", u[0], u[1]))
				print("not ok sentence", notOKSentence)
				notOK = resolution(self.kb, notOKSentence)
				if not notOK:
					print("not ok sentence")
					print(u)
					goals.add(u)
			if len(goals) > 0:
				allowed = copy.deepcopy(self.ok).union(goals)
				adjList = self.constructGraph(allowed)
				result = aStarSearch(self.p, goals, adjList)
				self.p = result['steps'][-1]
				self.plan.extend(result['plan'])

				# update the knowledge base of current place
				ok = (makePerceptSentence("OK", self.p[0], self.p[1]))
				self.kb.extend(ok.cnf())

		if len(self.plan) == 0:
			adjList = self.constructGraph(self.ok)
			result = aStarSearch(self.p, {(1,1)}, adjList)
			self.p = result['steps'][-1]
			self.plan.extend(result['plan'])
			self.plan.append(Act.EXIT_CAVE)	

	def updateWorldState(self):
		neis = neighbors(self.p[0], self.p[1], self.size[0], self.size[1])
		neis.append(self.p)
		for pos in neis:
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
					self.worldState[pos].add("PW")
		# mark the current position as visited			
		if self.p in self.unvisited: 
			self.unvisited.remove(self.p)

	def planRoute(self, current, goals):
		actions = []
		return actions

	def act(self):
		print("before act's plan", self.plan)
		result = {}
		perceptsToRemove = { }
		# tell if the agent wants to exit
		result['exit'] = self.plan[-1] == Act.EXIT_CAVE 
		while len(self.plan) > 0:
			if self.plan[0] == Act.STEP:
				self.move()
			elif self.plan[0] == Act.GRAB_GOLD:
				perceptsToRemove["G"] = self.p
				self.pickGold()
			elif self.plan[0] == Act.SHOOT_ARROW:
				perceptsToRemove["W"] = self.p
				self.shootArrow()
			self.plan.pop(0)
		result['perceptsToRemove'] = perceptsToRemove
		return result

	def do(self, world):
		self.updateKB(world)
		self.updateWorldState()
		print(self.kb)
		print("unvisited", self.unvisited)
		print("ok", self.ok)
		self.makePlan(world)
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

	def move(self):
		self.moveCnt -= Act.STEP.value
		# 	self.p[1] += 1 
		# elif act == Act.DOWN:
		# 	self.p[1] -= 1
		# elif act == Act.LEFT:
		# 	self.p[0] -= 1 
		# else:
		# 	self.p[0] += 1


		 

