from random import randint
import copy

class Gamefield:
	def __init__(self, gamefieldSize = 3):
		self.gamefieldSize = gamefieldSize
		self.gamefield = [[0 for j in range(0, self.gamefieldSize)] for i in range(0, self.gamefieldSize)]
		self.score = 0

	def addNewBlockAtRandomPosition(self, blockValue = 2):
		while True:
			randomX = randint(0, (self.gamefieldSize) - 1)
			randomY = randint(0, (self.gamefieldSize) - 1)
			cellContent = self.gamefield[randomX][randomY]
			if cellContent == 0:
				self.gamefield[randomX][randomY] = blockValue
				break

	def isGamefieldFull(self):
		for y in range(0, self.gamefieldSize):
			for x in range(0, self.gamefieldSize):
				if self.gamefield[x][y] == 0:
					return True
		return False
	
	def mergeBlocksHorizontally(self, direction=0):
		newGamefield = copy.deepcopy(self.gamefield)
		for y in range(0, self.gamefieldSize):
			basePointer = 0
			xCoordinates = range(1, self.gamefieldSize)

	
			if(direction == 1):
				basePointer = self.gamefieldSize - 1
				xCoordinates = range(self.gamefieldSize - 2, -1, -1)
			
			for x in xCoordinates:
				currentBlockValue = newGamefield[x][y]
				if currentBlockValue != 0:
					baseBlockValue = newGamefield[basePointer][y]
					if baseBlockValue == 0:
						newGamefield[basePointer][y] = currentBlockValue
						newGamefield[x][y] = 0
					else:
						if baseBlockValue == currentBlockValue:
							newGamefield[basePointer][y] = currentBlockValue * 2
							newGamefield[x][y] =  0
							self.score = self.score + currentBlockValue * 2
						else:
							if(direction == 0):
								basePointer = basePointer + 1
							else:
								basePointer = basePointer - 1
							if(basePointer != x):
								newGamefield[basePointer][y] = currentBlockValue
								newGamefield[x][y] = 0
		return newGamefield 

	def mergeBlocksVertically(self, direction=0):
		newGamefield = copy.deepcopy(self.gamefield)

		for y in range(0, self.gamefieldSize):
			basePointer = 0
			xCoordinates = range(1, self.gamefieldSize)

	
			if(direction == 1):
				basePointer = self.gamefieldSize - 1
				xCoordinates = range(self.gamefieldSize - 2, -1, -1)
			
			for x in xCoordinates:
				currentBlockValue = newGamefield[y][x]
				if currentBlockValue != 0:
					baseBlockValue = newGamefield[y][basePointer]
					if baseBlockValue == 0:
						newGamefield[y][basePointer] = currentBlockValue
						newGamefield[y][x] = 0
					else:
						if baseBlockValue == currentBlockValue:
							newGamefield[y][basePointer] = currentBlockValue * 2
							newGamefield[y][x] = 0
							self.score = self.score + currentBlockValue * 2
						else:
							if(direction == 0):
								basePointer = basePointer + 1
							else:
								basePointer = basePointer - 1
							if(basePointer != x):
								newGamefield[y][basePointer] = currentBlockValue
								newGamefield[y][x] = 0
		return newGamefield

	def compareGamefields(self, other):
		if len(self) != len(other):
			return False

		for y in range(0, len(self)):
			if len(self[y]) != len(other[y]):
				return False

			for x in range(0, len(self[y])):
				if self[y][x] != other[y][x]:
					return False
		return True
