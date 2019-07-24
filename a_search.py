from helper import distance
from heapq import heappush, heappop
def aStarSearch(start, goals, adjList):
	return None
	heap = []
	heappush(heap, ( sorted([distance(start, goal) for goal in goals][0], start )))

	current = start
	while heap:
		if current in goals:
			# calculate plans
			return

		current = heappop(heap)
		for nei in adjList[current]:
			priority = distFromCurrent + distToGoal
			heappush(heap, (priority, nei))
