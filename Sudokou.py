import random
import pygame
import os
import time


pygame.font.init()

WIDTH,HEIGHT = 500,500


WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

main_font = pygame.font.SysFont("comicsans", 45)
pygame.display.set_caption("Sudoku")


class Puzzle:
	def __init__(self):
		self.board =[[0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
				 	 [0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
		 		 	 [0,0,0,0,0,0,0,0,0],
		 			 [0,0,0,0,0,0,0,0,0]]
		 
		self.input_cell_positions = []


	def create_collum(self,collumn):
		coll = []
		for i in range(0,9):
			coll.append(self.board[i][collumn])
		return coll

	def create_row(self,row):
		return self.board[row]

	def create_box(self,r, c):
		#Detect what quadrant the point lies in and create a box based on the corner of that quadrant

		#row = 0 if row < 3, row = 3 if row < 6, row = 6 if row < 9
		row = 3 * int(r/3)
		#col = 0 if col < 3, col = 3 if col < 6, col = 6 if col < 9
		col = 3 * int(c/3)

		box = []
		for i in range(row,row + 3):
			for k in range(col,col + 3):
				box.append(self.board[i][k])
		return box

	def isPositionValid(self,r,c):
		val = self.board[r][c]
		#Create the rows,collumns,and boxes. [:] means to create a copy as to not change the orginal board
		row = self.create_row(r)[:]
		collumn = self.create_collum(c)[:]
		box = self.create_box(r,c)[:]

		#Delete the value board[r][c] from the respective lists in order to check if the lists contain the same value again
		del row[c]
		del collumn[r]
		del box[box.index(val)]


		#Traverse through the lists and check if they contain the same value twice
		for i in range(0,8):
			if row[i] == val or collumn[i] == val or box[i] == val:
				return False
		return True 


	def create_puzzle(self,row=0,col=0):
		if col == len(self.board):
			col = 0
			row += 1

		if row == len(self.board):
			self.remove_values()
			return True


		for x in range(0,9):
			self.board[row][col] = random.randrange(1,10)
			if self.isPositionValid(row, col):
				if self.create_puzzle(row, col + 1):
					return self.board

		self.board[row][col] = ''

	def solve(self,row=0,col=0):
		if col == len(self.board):
			col = 0
			row += 1

		if row == len(self.board):
			return True

		#If the row and collumn are in the input_cell_positions, then the spot should be solved for
		if (row,col) in self.input_cell_positions:
			for x in range(1,10):
				self.board[row][col] = x
				if self.isPositionValid(row, col):
					if self.solve(row, col + 1):
						return True	

			self.board[row][col] = ''
			return False

		else:
			if self.solve(row, col + 1):
				return True	

	#Removes random values from the board and sets them to ''
	#Appends the blank value positions to self.input_cell_positions
	def remove_values(self):
		for i in range(0,9):
			for k in range(0,9):
				if random.randrange(0,2) == 1:
					self.board[i][k] = ''
					self.input_cell_positions.append((i,k))

	def isSolved(self):
		for i in range(0,9):
			for k in range(0,9):
				if not self.isPositionValid(i,k):
					return False
		return True

	def print(self):
		for x in range(0,9):
			print(self.board[x])



class Game:
	def __init__(self):
		#the position of the cell ((row,col)) that the player wants to input into 
		self.input_cell = None

		#boolean displaing if the board is solved or not
		self.isSolved = False

		#creates the first puzzle and stores it in current
		self.current = Puzzle()
		self.current.create_puzzle()

	#Display's the board using the display_num function
	def display_board(self):
			for i in range(0,9):
				for k in range(0,9):
					#Need to pass the number as string in order to display it
					 self.display_num(f"{self.current.board[i][k]}", (i,k), (0,0,0))

	#This function takes in the number, it's position in the board, it's color, and the main font to display each number
	def display_num(self, number, position, color):
		#create number label (string)
		label_number = main_font.render(number, 1, color)

		#get the width and height of the label_number
		num_width = label_number.get_width()
		num_height = label_number.get_height()

		# 1.) Divide the WIDTH and HEIGHT of the screen to get each individual cell
		# 2.) Then, divide that by the width / height of each number
		# 3.) The second part of expression determines what cell the number should be in
		#         EX. If number is in 0th row, and 1st collumn then, (1 * (WIDTH/9) + 15) = x
		#                                                            (0 * (HEIGHT/9) + 15) = y
		# 4.) The +15 is there because the coordinates of the label_number are not centered, but to the left in python
		number_x = (WIDTH / 9) / num_width + (position[1] * (WIDTH / 9) + 15)
		number_y = (HEIGHT / 9) / num_height + (position[0] * (HEIGHT / 9) + 15)

		WINDOW.blit(label_number, (number_x, number_y))

		

	#Solves the current puzzle in the puzzles list. sets self.isSolved to true
	def solve(self):
		#Need to make all the input_cell_positions of the board back to '', so that the sudoku board is still solvable
		for row,col in self.current.input_cell_positions:
			self.current.board[row][col] = ''

		self.current.solve()
		self.isSolved = True


	#Displays the green rectangle over empty cell that player is hovering over
	def display_hover_over(self):
		#Get's the coordinates of of the cell that the player's mouse is closest to
		cell_coordinates = self.get_nearest_cell_coord(pygame.mouse.get_pos()) 
		

		#Set's rectangle to a rectangle at the nearest cell coordinates
		rectangle = self.get_cell_rect(cell_coordinates)

		# 1.) Iterates through the current board's list of self.input_cell_positions
		# 2.) Divides the current cell_coordinates (goes by iterations of (WIDTH or HEIGHT / 9) by (WIDTH and HEIGHT / 9) in order to bring them back down to their original positions
		# 3.) If their original positions are equal to the (row,col) of the input_cell_positions, the set the self.input_cell to that (row,col) and draw the rectangle at the cell_coordinates
		# 4.) If the player is not hovering over any empty cell, then self.input_cell is set to None
		if not self.isSolved:
			for row,col in self.current.input_cell_positions:
				if round(cell_coordinates[0] / (WIDTH / 9)) == col and round(cell_coordinates[1] / (HEIGHT / 9)) == row:
					self.input_cell = (row,col)
					pygame.draw.rect(WINDOW, (0,255,0), rectangle, 4)
					return 
			self.input_cell = None
			
	
	#Returns the coordinates of the cell closest to the players mouse position by dividing the (x,y) positions by the (WIDTH and HEIGHT / 9)  then multiplying them by the (WIDTH and HEIGHT / 9) for the exact cell position
	def get_nearest_cell_coord(self, position):
		return (round(WIDTH / 9) * int(position[0] / round(WIDTH / 9)), round(HEIGHT / 9) * int(position[1] / round(HEIGHT / 9)))

	#Returns rectangle at the cell_coordinates. The size of the rectnagle is (WIDTH/9) by (HEIGHT/9) so that the rectangle fully borders the cell
	def get_cell_rect(self, coordinates):
		return pygame.Rect(coordinates[0], coordinates[1], round(WIDTH/9), round(HEIGHT/9))

	#Sets the value at the current empty input_cell for the current puzzle to the parameter passed in
	def set(self, value):
		self.current.board[self.input_cell[0]][self.input_cell[1]] = value


def draw_grid():
	scale = round(WIDTH/9)

	for i in range(9):
		bold = 1
		if i % 3 == 0 and i != 0:
			bold = 4

		pygame.draw.line(WINDOW, (0,0,0), (i * scale, 0), (i * scale , HEIGHT ), bold)
		pygame.draw.line(WINDOW, (0,0,0), (0, i * scale), (WIDTH , i * scale), bold)

def draw_wrong():
	X = pygame.image.load(os.path.join("assets", "Red_X.png"))
	WINDOW.blit(X, (WIDTH/2 - X.get_width() / 2, HEIGHT/2 - X.get_width()/2))
	pygame.display.update()
	pygame.time.wait(1000)

def draw_correct():
	CHECK = pygame.image.load(os.path.join("assets", "Green_Check.png"))
	WINDOW.blit(CHECK, (WIDTH/2 - CHECK.get_width() / 2, HEIGHT/2 - CHECK.get_width()/2))
	pygame.display.update()
	pygame.time.wait(1000)

def main():
	run = True
	FPS = 60

	sudoku = Game()

	#Empty number that user will input
	input_number = ''

	#If the user has clicked on an empty cell or not
	active = False

	#redraws the elements in the window
	def redraw_window():
		WINDOW.fill((255,255,255))

		draw_grid()

		sudoku.display_board()

		sudoku.display_hover_over()

		#If the player does not hover over a cell that is occupied, display their input_number
		if sudoku.input_cell != None:
			sudoku.display_num(input_number, sudoku.input_cell, (169,169,169))

		pygame.display.update()

	
	while run:
		redraw_window()
		position = pygame.mouse.get_pos()

		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				run = False

				
			if event.type == pygame.KEYDOWN:
				if sudoku.input_cell != None:	
					if event.key == pygame.K_BACKSPACE:
						sudoku.set('')

					if event.key == pygame.K_RETURN and input_number.isdigit():
						sudoku.set(int(input_number))
						input_number = ''

					else:
						input_number = event.unicode


				if event.key == pygame.K_SPACE:
					sudoku.solve()

				if event.key == pygame.K_n:
					sudoku = Game()

				if event.key == pygame.K_c:
					if sudoku.current.isSolved():
						if not sudoku.isSolved:
							draw_correct()
					else:
						draw_wrong()
					

		if input_number.isalpha():
			input_number = ''

def main_menu():
	run = True
	title_font = pygame.font.SysFont("algerian", 75)
	title_label = title_font.render("Sudoku!", 2, (255,255,255))

	instruction_font = pygame.font.SysFont("algerian", 25)
	N_label = instruction_font.render("Press N for a new puzzle", 1, (255,255,255))
	C_label = instruction_font.render("Press C to check your puzzle", 1, (255,255,255))
	space_label = instruction_font.render("Press SPACE to solve the puzzle", 1, (255,255,255))

	while run:
		WINDOW.fill((0,0,0))
		WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, HEIGHT/9))
		WINDOW.blit(N_label, (WIDTH/2 - N_label.get_width()/ 2, HEIGHT / 3))
		WINDOW.blit(C_label, (WIDTH/2 - C_label.get_width()/ 2, HEIGHT/2))
		WINDOW.blit(space_label, (WIDTH/2 - space_label.get_width()/ 2, HEIGHT/1.5))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				main()


if __name__ == "__main__":
	main_menu()
