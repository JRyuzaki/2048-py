import curses 
import math
from random import random
import sys
import time 
import getopt
import base64 

from pathlib import Path
from Gamefield2048 import Gamefield


gamefieldSize = 3
blockSize = 6

winningString = ["__  __                                   ", "\ \/ /___  __  __   _      ______  ____  ", " \  / __ \/ / / /  | | /| / / __ \/ __ \ ", " / / /_/ / /_/ /   | |/ |/ / /_/ / / / / ", "/_/\____/\__,_/    |__/|__/\____/_/ /_/  "]
gameoverString = ["   ____                         ___                 ", "  / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __  ", " | |  _ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__| ", " | |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |    ", "  \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|    ", "                                                     "]

highscore = 0
highscoreFilename = ".highscore"

def readHighscore():
	highscoreFile = Path(highscoreFilename)
	if highscoreFile.is_file():
		highscoreFile = open(highscoreFilename, "r")
		highscoreHashString = highscoreFile.readline()
		try:
			global highscore
			highscore = int(highscoreHashString)
		except ValueError:
			highscore = 0

def writeHighscore(score):
	highscoreFile = Path(highscoreFilename)
	highscoreFile = open(highscoreFilename, "w+")
	highscoreFile.write(str(score))


def initializeCurses():
	global stdscr
	stdscr = curses.initscr()
	stdscr.keypad(1)
	
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_YELLOW)
	curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(6, curses.COLOR_WHITE, 233)
	curses.init_pair(7, 236, 236)
	curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)

def calculateMinimalRequiredDimensions():
	minimalWidth = gamefieldSize * blockSize * 3
	minimalHeight = gamefieldSize * blockSize + gamefieldSize
	return (minimalWidth, minimalHeight)

def randomlyInitializeGamefield(numberOfElements = 2):
	for i in range(0, numberOfElements):
		gamefield.addNewBlockAtRandomPosition()

def displayCursesGamefield():
	stdscr.addstr(0, 1, centerStringToSize(" ", minimalRequiredScreenWidth), curses.color_pair(7))
	stdscr.addstr(minimalRequiredScreenHeight, 0, centerStringToSize(" ", minimalRequiredScreenWidth + 2), curses.color_pair(7))

	for y in range (0, gamefield.gamefieldSize):
		for x in range(0, gamefield.gamefieldSize):
			for i in range(0, blockSize + 1):
				stdscr.addstr(y * (blockSize + 1) + i, 0, " ", curses.color_pair(7))
				stdscr.addstr(y * (blockSize + 1) + i, minimalRequiredScreenWidth, " ", curses.color_pair(7))		
			
			fieldValue = gamefield.gamefield[x][y]		
			if fieldValue <= 0:
				continue
			
			colorCode = int((math.log(fieldValue, 2) + 1) / 2)
	
			if colorCode > 6:
				colorCode = 6
	
			for i in range(0, blockSize):
				if i != int(blockSize / 2):
					stdscr.addstr(y * blockSize + i + y + 1, x * blockSize * 3 + 2, centerStringToSize(" ", blockSize * 3 - 2), curses.color_pair(colorCode))
				else:
					stdscr.addstr(y * blockSize + i + y + 1, x * blockSize * 3 + 2, centerStringToSize(str(fieldValue), blockSize * 3 - 2), curses.color_pair(colorCode))

	scoreString = "SCORE: " + str(gamefield.score)

	if gamefield.gamefieldSize == 4:
		scoreString = scoreString + " \t\t HIGHSCORE: " + str(highscore)	
	
	stdscr.addstr(minimalRequiredScreenHeight + 1, 0, scoreString)

	stdscr.addstr(minimalRequiredScreenHeight + 2, 0, "Press [Q] to quit \t\t Controls: W/A/S/D")

def centerStringToSize(string, size, fillChar=" "):
	if (size - len(string)) < 0:
		return string 

	iterationSize = size - len(string)
	for i in range(0, iterationSize):
		if len(string) + 1 >= size:
			break
		else:
			if i % 2 == 0:
				string = string + " "
			else:
				string  = " " + string
	
	return string 

def endCurses():
	curses.echo()
	curses.nocbreak()
	curses.curs_set(1)
	curses.endwin()

def displayDialogue(stringArray, colorPairIndex, displayDuration = 2):
	textX = int((screenWidth - len(stringArray[0])) / 2)
	textY = int((screenHeight - len(stringArray)) / 2)

	stdscr.clear()

	for i in range(0, len(stringArray)):
		stdscr.addstr(textY + i, textX, stringArray[i], curses.color_pair(colorPairIndex))

	stdscr.refresh()
	time.sleep(displayDuration)

def handleArguments(args):
	for i in range(0, len(args)):
		arg = args[i]
		if arg == "-s":
			if (i + 1) < len(args):
				try:
					global gamefieldSize
					gamefieldSize = max(int(args[i + 1]), 2)
					i = i + 1
				except ValueError:
					continue
		elif arg == "-w":
			if i + 1 < len(args):
				try:
					global blockSize
					blockSize = max(int(args[i + 1]), 1)
					i = i + 1
				except ValueError:
					continue

def isGameWon():
	for y in range(0, gamefieldSize):
		for x in range(0, gamefieldSize):
			if gamefield.gamefield[x][y] >= 2048:
				return True
	return False



handleArguments(sys.argv)
initializeCurses()

screenWidth = curses.COLS
screenHeight = curses.LINES
minimalRequiredScreenWidth, minimalRequiredScreenHeight = calculateMinimalRequiredDimensions()

if minimalRequiredScreenWidth > screenWidth or minimalRequiredScreenHeight > screenHeight:
	endCurses()
	sys.exit("Size of terminal is too small for this size of gamefield\nTry again with a smaller one")

gamefield = Gamefield(gamefieldSize)
randomlyInitializeGamefield(2)


if gamefield.gamefieldSize == 4:
	readHighscore()

gameRunning = True
gameWon = False

while gameRunning:
	stdscr.clear()

	try:
		displayCursesGamefield()
	except Exception:
		break

	possibleNextMoves = [gamefield.mergeBlocksVertically(), gamefield.mergeBlocksVertically(1), gamefield.mergeBlocksHorizontally(), gamefield.mergeBlocksHorizontally(1)]
	amountOfValidNextMoves = len(possibleNextMoves)
	for i in range(0, len(possibleNextMoves)):
		if Gamefield.compareGamefields(gamefield.gamefield, possibleNextMoves[i].gamefield):
			possibleNextMoves[i] = None 
			amountOfValidNextMoves = amountOfValidNextMoves - 1

	if amountOfValidNextMoves == 0:	
		displayDialogue(gameoverString, 9)
		break

	try:
		userInputCode = stdscr.getch()
	except:
		gameRunning = False
		break

	newGamefield = None
	if userInputCode == ord("s") or userInputCode == curses.KEY_DOWN:
		newGamefield = possibleNextMoves[1]
	elif userInputCode == ord("w") or userInputCode == curses.KEY_UP:
		newGamefield = possibleNextMoves[0]
	elif userInputCode == ord("d") or userInputCode == curses.KEY_RIGHT:
		newGamefield = possibleNextMoves[3]
	elif userInputCode == ord("a") or userInputCode == curses.KEY_LEFT:
		newGamefield = possibleNextMoves[2]
	elif userInputCode == ord("q"):
		gameRunning = False
	else:
		continue
	
	if newGamefield == None:
		continue

	gamefield = newGamefield
	
	if not gameWon:
		gameWon = isGameWon()
		if gameWon: 
			displayDialogue(winningString, 8)

	blockValue = 2
	if random() < 0.1:
		blockValue = 4
	gamefield.addNewBlockAtRandomPosition(blockValue)

	if gamefield.gamefieldSize == 4 and gamefield.score > highscore:
		highscore = gamefield.score
		writeHighscore(highscore)
	
	stdscr.refresh()
endCurses()
