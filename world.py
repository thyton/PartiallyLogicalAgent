class World:
	def __init__(self, w, h, problem, percepts):
		self.w = w
		self.h = h
		self.problem = problem
		self.percepts = percepts       # list of all possible percepts

	def perceptsAt(self, p):
		return self.problem[p]

	def removeGold(self, p):
		if "G" in self.problem[p]:
			 self.problem[p].remove("G")
