from enum import Enum
# from pygame.locals import *
import pygame
import pygame as pg

from pyPL import *
from world import World
from helper import *
from agent import Agent

screenW, screenH  = 1000, 675

pg.init()

black = (0,0,0)
white = (255,255,255)
blue = (0, 128, 255)
margin = 1
sqrSide = 60 

screen = pg.display.set_mode((screenW, screenH))
screen.fill(black)
# title
pg.display.set_caption("A Logical Agent Exploring Wumpus World - Thy Ton")

# init problem
problem = readProblem("problem_4b4.txt")
percepts = {"W", "P", "S", "B"}
h,w = 4,4
world = World(h, w, problem, percepts)

# show rect using real x and y from pygame standard
showRect = lambda color, x, y, w, h \
			: pg.draw.rect(screen\
			, color, [x, y, w, h])

# show line using real x and y from pygame standard
showLine = lambda color, x0, y0, x1, y1 \
			: pg.draw.line(screen\
			, color, (x0, y0), (x1, y1))

# show square at wumpus world position x, y
showSquare = lambda color, x, y \
			: pg.draw.rect(screen\
			, color\
			, [(margin + sqrSide) * (x-1) + margin\
			, (margin + sqrSide) * (y-1) + margin\
			, sqrSide\
			, sqrSide])


# draw grid 
for x in range(1, 11):
	for y in range(1, 11):
		showSquare(white, x, y)
# images
agentImg =  pg.image.load('images/agent.png')
goldImg =  pg.image.load('images/gold.png')
breezeImg =  pg.image.load('images/breeze.jpg')
pitImg =  pg.image.load('images/pit.gif')
stenchImg =  pg.image.load('images/stench.png')
wumpusImg =  pg.image.load('images/wumpus.jpg')
images = {'A': agentImg\
		, 'G': goldImg\
		, 'B': breezeImg\
		, 'P': pitImg\
		, 'S': stenchImg\
		, 'W':wumpusImg\
		,}
for name in images:
	images[name] = pg.transform.scale(images[name], (sqrSide, sqrSide))

# show image at x, y of pygame standard
showImage = lambda img, x, y \
					: screen.blit(img\
					, (x, y))

realXY = lambda gridX, gridY\
				:[(margin+sqrSide) * (gridX-1) + margin\
					, (margin+sqrSide) * (gridY-1) + margin]
# show image at x, y of wumpus problem 
showImageAtGrid = lambda img, x, y \
					: screen.blit(img\
					, ((margin+sqrSide) * (x-1) + margin\
					, (margin+sqrSide) * (y-1) + margin))

# draw the bottom margin for the grid
gridBottomMargin = 4
bottomMarginX = 0
bottomMarginY = (margin + sqrSide)*h + margin
showRect(blue, bottomMarginX, bottomMarginY, bottomMarginY, gridBottomMargin)

# current percept bar below the grid's bottom margin
percBarX = 0
percBarY = bottomMarginY + gridBottomMargin

# show image at x, y of wumpus problem 
showImageAtPercBar = lambda img, x\
					: screen.blit(img\
					, [(margin+sqrSide) * (x-1) + margin\
					,  percBarY])

clock = pg.time.Clock()
def smoothMoveImage(img, oldX, oldY, x, y):
	""" 
		Moves image vertically or horizontally in a smooth way
	"""
	if oldX != x and oldY != y:
		return
	if oldX == x:
		if y > oldY:
			k = 1
			funcRunning = True
			while funcRunning:
				funcRunning =  not(k == margin + sqrSide)
				for event in pg.event.get():
					if event.type == pg.QUIT:
						funcRunning = False
				# erase the image from at the previous location
				showRect(white, oldX, oldY + k - 1, sqrSide, sqrSide)
				# draw the image at the new location
				showImage(img, oldX, oldY + k)
				pg.display.update()
				# wait approx 1/sqrSide seconds before render next frame
				clock.tick(sqrSide)
				k += 1
			showLine(black, x, y - 1, x + sqrSide, y - 1)
			pg.display.update()
		elif y < oldY:
			i = 1
			funcRunning = True
			while funcRunning:
				funcRunning =  not(i == margin + sqrSide)
				for event in pg.event.get():
					if event.type == pg.QUIT:
						funcRunning = False
				# erase the image from at the previous location				
				showRect(white, oldX, oldY - i + 1, sqrSide, sqrSide)
				# draw the image at the new location
				showImage(img, oldX, oldY - i)
				pg.display.update()
				# wait approx 1/sqrSide seconds before render next frame
				clock.tick(sqrSide)
				i += 1
			showLine(black, x, oldY - 1, x + sqrSide, oldY - 1)
			pg.display.update()
	else: # that y == oldY
		if x > oldX:
			k = 1
			funcRunning = True
			while funcRunning:
				funcRunning =  not(k == margin + sqrSide)
				for event in pg.event.get():
					if event.type == pg.QUIT:
						funcRunning = False
				# erase the image from at the previous location				
				showRect(white, oldX + k - 1, oldY, sqrSide, sqrSide)
				# erase the image from at the previous location				
				showImage(img, oldX + k, oldY)
				pg.display.update()
				# wait approx 1/sqrSide seconds before render next frame
				clock.tick(sqrSide)
				k += 1
			showLine(black, x - 1, y, x - 1, y + sqrSide)	
			pg.display.update()
		else:
			k = 1
			funcRunning = True
			while funcRunning:
				funcRunning =  not(k == margin + sqrSide)
				for event in pg.event.get():
					if event.type == pg.QUIT:
						funcRunning = False
				# erase the image from at the previous location				
				showRect(white, oldX - k + 1, oldY, sqrSide, sqrSide)
				# erase the image from at the previous location				
				showImage(img, oldX - k, oldY)
				pg.display.update()
				# wait approx 1/sqrSide seconds before render next frame
				clock.tick(sqrSide)
				k += 1
			showLine(black, oldX - 1, y, oldX - 1, y + sqrSide)	
			pg.display.update()

a = Agent(h, w)
preAgentPos = a.p
running = True
clock = pg.time.Clock()
while running:
	# # erase the old agent and draw new agent
	# showSquare(white, *preAgentPos)
	# showImageAtGrid (images['A'], *a.p)

	# erase the old percepts and draw new percepts at the screen bottom
	showRect(black, percBarX, percBarY, bottomMarginY, sqrSide)
	x = 1
	for percept in problem[a.p]:
		if percept != 'A':
			showImageAtPercBar(images[percept], x)
			x+=1	
	pg.display.update()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
	if running:
		result = a.do(world)
		print(result['steps'])
		for i in range(len(result['steps']) - 1):
			oldXY = realXY(*result['steps'][i])
			newXY = realXY(*result['steps'][i + 1])
			smoothMoveImage(images["A"], *oldXY, *newXY)
		running = False

		for percept, position in result['perceptsToRemove'].items():
			if percept in problem[position]:
					problem[position].remove(percept)
					print("problem position", problem[position])
		running = not result['exit']
		
		if running and "P" in problem[a.p] or "W" in problem[a.p] or a.moveCnt < 0:
			a.die()
			running = False

		if not running:
			clock.tick(30)
print("Agent score:", a.score)
print("Move Cnt", a.moveCnt)
pg.quit()
quit()