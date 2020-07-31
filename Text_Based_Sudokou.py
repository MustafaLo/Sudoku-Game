import random


board = [[0,0,0,2,6,0,7,0,1],
		 [6,8,0,0,7,0,0,9,0],
		 [1,9,0,0,0,4,5,0,0],
		 [8,2,0,1,0,0,0,4,0],
		 [0,0,4,6,0,2,9,0,0],
		 [0,5,0,0,0,3,0,2,8],
		 [0,0,9,3,0,0,0,7,4],
		 [0,4,0,0,5,0,0,3,6],
		 [7,0,3,0,1,8,0,0,0]]
'''
board = [[4,3,5,2,6,9,7,8,1],
		 [6,8,2,5,7,1,4,9,3],
		 [1,9,7,8,3,4,5,6,2],
		 [8,2,6,1,9,5,3,4,7],
		 [3,7,4,6,8,2,9,1,5],
		 [9,5,1,7,4,3,6,2,8],
		 [5,1,9,3,2,6,8,7,4],
		 [2,4,8,9,5,7,1,3,6],
		 [7,6,3,4,1,8,2,5,9]]
'''


def createCollum(collumn):
	coll = []
	for i in range(0,9):
		coll.append(board[i][collumn])
	return coll

def createRow(row):
	return board[row]

def createBox(r, c):
	#Detect what quadrant the point lies in and create a box based on the corner of that quadrant

	#row = 0 if row < 3, row = 3 if row < 6, row = 6 if row < 9
	row = 3 * int(r/3)
	#col = 0 if col < 3, col = 3 if col < 6, col = 6 if col < 9
	col = 3 * int(c/3)

	box = []
	for i in range(row,row + 3):
		for k in range(col,col + 3):
			box.append(board[i][k])
	return box

def isPositionValid(r,c):
	val = board[r][c]
	#Create the rows,collumns,and boxes. [:] means to create a copy as to not change the orginal board
	row = createRow(r)[:]
	collumn = createCollum(c)[:]
	box = createBox(r,c)[:]

	#Delete the value board[r][c] from the respective lists in order to check if the lists contain the same value again
	del row[c]
	del collumn[r]
	del box[box.index(val)]


	#Traverse through the lists and check if they contain the same value twice
	for i in range(0,8):
		if row[i] == val or collumn[i] == val or box[i] == val:
			return False
	return True 

'''
def isSolved():
	nums = [1,2,3,4,5,6,7,8,9]
	collIterator,boxIterator1,boxIterator2 = 0;
	
	#Check if rows are correct
	for row in board:
		if not(set(row) == set(nums)):
			return False

	while collIterator < 9 and boxIterator2 < 7:
		#Build out rows and boxes
		coll = createCollum(collIterator)
		box = createBox(boxIterator1, boxIterator2)

		if (not set(coll) == set(nums)):
			return False

		if not set(box) == set(nums):
			return False
			break

		collIterator += 1

		if boxIterator1 < 6:
			boxIterator1 +=3 
		else:
			boxIterator2 += 3
			boxIterator1 = 0

	return True
'''

def isSolved():
	for i in range(0,9):
		for k in range(0,9):
			if not isPositionValid(i,k):
				return False
	return True


def solveBoard(row=0,col=0):

	if col == len(board):
		col = 0
		row += 1

	if row == len(board):
		return True

	if board[row][col] == 0:
		for x in range(1,10):
			print(f"Row: {row}")
			print(f"Col: {col}")
			print(f"X: {x}")
			board[row][col] = x
			
			if isPositionValid(row, col):
				if solveBoard(row, col + 1):
					return True	

		board[row][col] = 0
		return False

	else:
		if solveBoard(row, col + 1):
			return True	


def printBoard():
	for x in range(0,9):
		print(board[x])

solveBoard()

if isSolved():
	printBoard()
