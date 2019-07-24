from enum import Enum
# import pygame
# from pygame.locals import *

from pyPL import *
from world import World
from helper import *
from agent import Agent

class Percept(Enum):
	G = 5 
	W = 4
	P = 3
	S = 2
	B = 1


# pygame.init()

# screen = pygame.display.set_mode((900, 500))

running = True

# # main loop
# while running:
#     # for loop through the event queue
#     for event in pygame.event.get():
#         # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
#         if event.type == KEYDOWN:
#             # If the Esc key has been pressed set running to false to exit the main loop
#             if event.key == K_ESCAPE:
#                 running = False
#         # Check for QUIT event; if QUIT, set running to false
#         elif event.type == QUIT:
#             running = False

problem = readProblem("problem.txt")
percepts = {"W", "P", "S", "B"}
world = World(10, 10, problem, percepts)
a = Agent(10, 10)

while running:
	perceptsToRemove = a.do(world)

	for percept, positions in perceptsToRemove.items():
		for p in positions:
			if percept in problem[p]:
				problem[p].remove(percept)

	running = "W" not in problem[a.p] and "P" not in problem[a.p] \
			and (a.moveCnt > 0 or a.p == (1,1))
	running = False

print("Agent score:", a.score)
