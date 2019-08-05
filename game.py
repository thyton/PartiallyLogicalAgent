"""
Wumpus game body
Thy Ton
"""

from enum import Enum
import pygame as pg

from pyPL import *
from world import World
from helper import *
from agent import Agent


# init problem
# h,w = 6,6
# problem = readProblem("problem_6b6.txt")
h,w = 4,4
problem = readProblem("problem_4b4.txt")
percepts = {"W", "P", "S", "B"}
world = World(h, w, problem, percepts)

black = (0,0,0)
white = (255,255,255)
blue = (0, 128, 255)
margin = 1
sqrSide = 50 
axisW = 30

# draw the bottom margin for the grid
gridBottomMargin = 10
bottomMarginX = axisW + margin
bottomMarginY = axisW + (margin + sqrSide)*h + margin

# percept bar below the grid's bottom margin
percBarX = axisW
percBarY = bottomMarginY + gridBottomMargin

# init screen
screenW, screenH  = 800, 600
pg.init()
screen = pg.display.set_mode((screenW, screenH))
screen.fill(black)

# title
pg.display.set_caption("A Partially Logical Agent Exploring Wumpus World - Thy Ton")

#clock
clock = pg.time.Clock()

#font
font = pg.font.SysFont(("Arial"),25)

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
			, [axisW + (margin + sqrSide) * (x-1) + margin\
			, (axisW + margin + sqrSide) * (y-1) + margin\
			, sqrSide\
			, sqrSide])

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

# show image at x, y of wumpus problem 
showImageAtPercBar = lambda img, x\
					: screen.blit(img\
					, [axisW + (margin+sqrSide) * (x-1) + margin\
					, percBarY])

# show image at x, y of pygame standard
showImage = lambda img, x, y \
					: screen.blit(img\
					, (x, y))

realXY = lambda gridX, gridY\
				:[axisW + (margin+sqrSide) * (gridX-1) + margin\
					, axisW + (margin+sqrSide) * (gridY-1) + margin]
# show image at x, y of wumpus problem 
showImageAtGrid = lambda img, x, y \
					: screen.blit(img\
					, (0 + (margin+sqrSide) * (x-1) + margin\
					, (0 + margin+sqrSide) * (y-1) + margin))


def smoothMoveImage(img, oldX, oldY, x, y, color):
	# Moves image vertically or horizontally in a smooth way
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
				showRect(color, oldX, oldY + k - 1, sqrSide, sqrSide)
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
				showRect(color, oldX, oldY - i + 1, sqrSide, sqrSide)
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
				showRect(color, oldX + k - 1, oldY, sqrSide, sqrSide)
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
				showRect(color, oldX - k + 1, oldY, sqrSide, sqrSide)
				# erase the image from at the previous location				
				showImage(img, oldX - k, oldY)
				pg.display.update()
				# wait approx 1/sqrSide seconds before render next frame
				clock.tick(sqrSide)
				k += 1
			showLine(black, oldX - 1, y, oldX - 1, y + sqrSide)	
			pg.display.update()


def showTextLine(words, startX, startY, lineW, lineSpace, color):
	spaceW = font.size(' ')[0]
	k = 1
	funcRunning = True
	x = startX
	y = startY
	while funcRunning:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				funcRunning = False
		for i in range(len(words)):
			wordSurface = font.render(words[i], True, color)
			wordW, wordH = wordSurface.get_size()
			# jump to the next row to display when row is overflowed
			if x + wordW - startX > lineW:
				x = startX
				y += wordH
			screen.blit(wordSurface, (x, y))
			x += wordW + spaceW
		pg.display.update()
		funcRunning = False

axisFont = pg.font.SysFont(("Narrow Arial"),30)
wordH = axisFont.size(str("1"))[1]
vertMarginWord = (axisW - wordH)/2
for x in range(1, w+1):
	wordW = axisFont.size(str(x))[0]
	horMarginWord = (axisW - wordW)/2
	showTextLine(str(x), axisW + (x-1)*sqrSide + margin + horMarginWord , axisW - wordH - vertMarginWord, sqrSide, 5, blue)
for y in range(1, h+1):
	wordW = axisFont.size(str(y))[0]
	horMarginWord = (axisW - wordW)/2
	showTextLine(str(y), horMarginWord, axisW + (y-1)*sqrSide + margin + vertMarginWord, sqrSide, 5, blue)

# draw grid
for x in range(1, h + 1):
	for y in range(1, w + 1):
		showRect(white, *realXY(x, y), sqrSide, sqrSide)

# percept bar top margin
showRect(blue, bottomMarginX, bottomMarginY, bottomMarginY-axisW, gridBottomMargin)
# title for percept bar
wordH = pg.font.SysFont(("Narrow Arial"),25).size(str("Current percepts"))[1]
showTextLine(str("Current percepts"), percBarX, percBarY, screenW - axisW, 5, white)
percBarY += wordH + 5

# score bar top margin
scoreBarY = percBarY + sqrSide
showRect(blue, bottomMarginX, scoreBarY, bottomMarginY-axisW, gridBottomMargin)
# title for percept bar
scoreBarY += gridBottomMargin
showTextLine(str("Score"), bottomMarginX, scoreBarY, screenW - axisW, 5, white)
scoreBarY += wordH + 5 

# score bar top margin
moveBarY = scoreBarY + wordH
showRect(blue, bottomMarginX, moveBarY, bottomMarginY-axisW, gridBottomMargin)
# title for score bar
moveBarY += gridBottomMargin
showTextLine(str("Move count"), bottomMarginX, moveBarY, screenW - axisW, 5, white)
moveBarY += wordH + 5 
showTextLine(str(0), axisW + margin, moveBarY, bottomMarginY-axisW, 2, blue)

# steps bar
stepsBarW = 200
stepsBarX = screenW - stepsBarW
stepsBarY = 0

a = Agent(h, w)
moveCnt = 0
preAgentPos = a.p
running = True
clock = pg.time.Clock()
while running:
	# erase the old percepts and draw new percepts at the screen bottom
	showRect(black, percBarX, percBarY, bottomMarginY-axisW, sqrSide)

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
		# erase the image from at the previous location				
		showRect(black, stepsBarX, 0, screenW - stepsBarX, screenH)
		wordH = font.size('s')[1]
		lineSpace = 2
		y = stepsBarY 
		agentMoves = False
		oldXY, newXY = 0,0
		if len(result['steps']) > 1:
			showTextLine("Route:".split(" "), stepsBarX,y, stepsBarW, lineSpace, white)
			y += wordH + lineSpace
		for i in range(len(result['steps'])):
			if result['steps'][i] == Act.SHOOT_ARROW:
				text = "Shoot an arrow at current position"
				showTextLine(text.split(" "), stepsBarX, y, stepsBarW, lineSpace, white)
			elif result['steps'][i] == Act.GRAB_GOLD:
				text = "Pick up gold at the current position"
				showTextLine(text.split(" "), stepsBarX, y, stepsBarW, lineSpace, white)
				# we don't display actions other than steps of agent
			elif i < len(result['steps']) - 1 and not isinstance(result['steps'][i+1], Act):
				text = str(result['steps'][i])+" -> "+str(result['steps'][i+1])
				oldXY = realXY(*result['steps'][i])
				newXY = realXY(*result['steps'][i + 1])
				agentMoves = True
				showTextLine(text.split(" "), stepsBarX, y, stepsBarW, lineSpace, white)
			pg.display.update()
			x = stepsBarX
			y += wordH + lineSpace

			if agentMoves:
				smoothMoveImage(images["A"], *oldXY, *newXY, blue)
				moveCnt += 1
				showRect(black, axisW + margin, moveBarY, bottomMarginY-axisW, scoreH)	
				showTextLine(str(moveCnt), axisW + margin, moveBarY, bottomMarginY-axisW, lineSpace, blue)
				agentMoves = False

		scoreH = pg.font.SysFont(("Narrow Arial"),25).size(str("Score"))[1]
		showRect(black, axisW + margin, scoreBarY, bottomMarginY-axisW, scoreH)	
		showTextLine(str(a.score), axisW + margin, scoreBarY, stepsBarW, lineSpace, blue)
		s = ""
		for percept, position in result['perceptsToRemove'].items():
			if percept in problem[position]:
				problem[position].remove(percept)
				s += percept + " "
		print("-")
		print(s)
		print(result)

		running = not result['exit']
		
		if running and "P" in problem[a.p] or "W" in problem[a.p] or a.moveCnt < 0:
			a.die()
			running = False

clock.tick(3000000)
pg.quit()
quit()