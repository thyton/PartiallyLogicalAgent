"""
A* Search 
Thy Ton
"""

from helper import distance, Act
from heapq import heappush, heappop

def aStarSearch(start, goals, adjList):
	heap = []
	fromStart = {}
	fromStart[start] = 0
	previousPos = {}
	heappush(heap, (min([distance(start, goal) for goal in goals]), start) )
	while heap:
		current = heappop(heap)[1]
		if current in goals:
			# calculate plans
			moveCnt = fromStart[current]
			steps = []
			pos = current
			while pos != start:
				steps.insert(0, pos)
				pos = previousPos[pos]
			steps.insert(0, start)
			return { 'steps' : steps, 'plan': [Act.STEP]*moveCnt}
		neis = adjList[current]
		for nei in neis:
			if nei not in fromStart:
				previousPos[nei] = current
				fromStart[nei] = fromStart[current] + 1 
				priority = fromStart[nei] + min([distance(nei, goal) for goal in goals])
				heappush(heap, (priority, nei))
			elif fromStart[current] + 1 < fromStart[nei]:
			# if there is a shorter path to nei
				fromStart[nei] = fromStart[current] + 1
				previousPos[nei] = current
				priority = fromStart[nei] + min([distance(nei, goal) for goal in goals])


