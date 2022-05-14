'''
CPSC 415 -- Homework #3.5
Morgan Conner, University of Mary Washington, fall 2021
'''

import sys
from random import randint
from copy import deepcopy
import numpy as np

class Queen():
	def __init__(self, name, board_length):
		self.notation = 'Q'
		self.name = name
		self.max_dist = board_length

	def get_notation(self):
		return self.notation

class Board():
	def __init__(self,cost=0):
		self.board = []
		self.board_cost = cost

	def create_board(self, size):
		board_list = [ ['.' for __ in range(size)] for __ in range(size)]
		return board_list

	def set_board(self, board):
		self.board = board

	def set_cost(self, cost):
		self.board_cost = cost

	def cost_evaluator(self, d_attacking_queens, v_attacking_queens, h_attacking_queens):
		cost = len(d_attacking_queens) + len(v_attacking_queens) + len(h_attacking_queens)
		return cost

def check_diagonal(board_length, queens_locations, d_attacking_queens):
	all_queens_plots = list(queens_locations.values())
	
	#checks if queens can attack others
	for item in queens_locations.items():
		queen_plot1 = item[1]
		queen_name1 = item[0]
		for value in all_queens_plots:
			if queen_plot1 == value:
				popped_item = value
				all_queens_plots.remove(value)
			elif abs(queen_plot1[0] - value[0]) == abs(queen_plot1[1] - value[1]):
				for x in queens_locations.items(): #cycles dict to get name of victum
					if x[1] == value:
						name = x[0]
				d_attacking_queens.append((queen_name1, name))

		all_queens_plots.append(popped_item) #make list original
	
	return d_attacking_queens

def check_vertical(board_length, queens_locations, v_attacking_queens):
	all_queens_plots = list(queens_locations.values())

	for item in queens_locations.items():
		queen_plot1 = item[1]
		queen_name1 = item[0]
		for value in all_queens_plots:
			if queen_plot1 == value:
				popped_item = value
				all_queens_plots.remove(value)
			elif queen_plot1[0] == value[0]:
				for x in queens_locations.items():
					if x[1] == value:
						name = x[0]
				v_attacking_queens.append((queen_name1,name))

		all_queens_plots.append(popped_item) #make list original
	
	return v_attacking_queens

def check_horizontal(board_length, queens_locations, h_attacking_queens):
	all_queens_plots = list(queens_locations.values())
	
	for item in queens_locations.items():
		queen_plot1 = item[1]
		queen_name1 = item[0]
		for value in all_queens_plots:
			if queen_plot1 == value:
				popped_item = value
				all_queens_plots.remove(value)
			elif queen_plot1[1] == value[1]:
				for x in queens_locations.items():
					if x[1] == value:
						name = x[0]
				h_attacking_queens.append((queen_name1,name))

		all_queens_plots.append(popped_item) #make list original
		
	return h_attacking_queens	

def steepest_hill_climbing(board, queen_piece, queens_locations, d_attacking_queens, v_attacking_queens, h_attacking_queens, board_length):
	cost_to_beat = board.board_cost
	new_queens_locations = {}
	board_obj_list = []
	best_unique_moves = {} #saves board and cost lower than cost_to_beat
	best_same_moves = [] #saves board and cost equal to cost_to_beat
	placement_list = list(queens_locations.values())
	name_list = list(queens_locations.keys())
	
	#Cycles through every col and row
	for item in placement_list:
		col = item[0]
		row = item[1]
		board_row = 0
		while board_row <= board_length - 1:
			#doesn't calc cost for current position
			if board_row == row:
				board_row += 1
				continue

			board_obj = Board()
			board_obj_list = board_obj.create_board(board_length)
			board_obj.set_board(board_obj_list)
			board_cpy = deepcopy(placement_list) #list of (x,y) values
			queens_locations_cpy = deepcopy(queens_locations) #dictionary of queens placements on board

			#updates the queens placements on board and saves them in dict
			board_cpy[col] = (col,board_row)
			q_name = name_list[col]
			queens_locations_cpy[q_name] = (col,board_row)

			#creates board in list form
			for item in board_cpy:
				col_temp = item[0]
				row_temp = item[1]
				board_obj_list[row_temp][col_temp] = queen_piece.get_notation()
			board_obj.set_board(board_obj_list)
			print(board_obj.board)

			#Gets board cost
			d_attacking_queens = check_diagonal(board_length, queens_locations_cpy, d_attacking_queens)
			v_attacking_queens = check_vertical(board_length,queens_locations_cpy, v_attacking_queens)
			h_attacking_queens = check_horizontal(board_length, queens_locations_cpy, h_attacking_queens)
			board_cpy_cost = board_obj.cost_evaluator(d_attacking_queens, v_attacking_queens, h_attacking_queens)
			d_attacking_queens.clear()
			v_attacking_queens.clear()
			h_attacking_queens.clear()

			#save board and cost to moves if it's lower than original board cost
			if board_cpy_cost < cost_to_beat:
				best_unique_moves[board_cpy_cost] = queens_locations_cpy
			elif board_cpy_cost == cost_to_beat:
				best_same_moves.append(queens_locations_cpy)
			else:
				queens_locations_cpy = {}
				best_same_moves = []
				board_cpy_cost = 0
			if 0 in best_unique_moves.keys():
				break
			board_row += 1
		if 0 in best_unique_moves.keys():
			break

	#Picks best move based on cost
	solution_to_display = []
	if len(best_unique_moves) > 0:
		for k,v in best_unique_moves.items():
			if k < cost_to_beat:
				cost_to_beat = k
				new_queens_locations = v
	elif len(best_same_moves) > 0:
		index = randint(0,len(best_same_moves)-1)
		picked_best_same_move = best_same_moves[index]
		new_queens_locations = picked_best_same_move
		
	solution_to_display = solution_list(new_queens_locations)
	
	return (new_queens_locations, solution_to_display, board_obj_list, cost_to_beat)

def solution_list(queens_locations):
	queens_place = list(queens_locations.values())
	raw_list = [] #used to make graphic
	if len(queens_place) == 0:
		config_list = []
	else:
		config_list = ['[']

		for item in queens_place:
			row_place = str(item[-1])
			config_list.append(row_place)
			raw_list.append(row_place)

		config_list.append(']')
		print(*config_list) #pretty list

	return (raw_list, config_list)

def show_graphic_solution(board_length, board_list, solution_to_display):
	raw_list = solution_to_display[0]
	theBoard = np.array(board_list)
	seperator = ['+']
	seperator.extend(('-'*(board_length - 2)))
	seperator.extend('+')
	
	print("\nSolution:")
	print(*seperator)
	for element in theBoard:
		print(*element)
	print(*seperator)

	print(*solution_to_display[1])

#--------MAIN---------------
argu = sys.argv[1]
num_of_queens = int(argu)
board_length = int(argu)

if num_of_queens < 4:
	print("Enter a number greater than three.")
	sys.exit(1)


#Creates random board and queen pieces
#print("Random restart will occur if solution is not found within 100 iterations.")
current_board = Board()
current_board_list = current_board.create_board(board_length)
current_board.set_board(current_board_list)
queens_locations = {}
d_attacking_queens, v_attacking_queens, h_attacking_queens = [],[],[]

for col in range(num_of_queens):
	name = 'queen' + str(col + 1)
	queen_piece = Queen(name, board_length)
	
	#Puts queens in different row randomly
	rand_row = randint(0,board_length - 1)
	current_board_list[rand_row][col] = queen_piece.get_notation()
	
	#saves queens location in dictionary
	queen_piece.location = (col,rand_row)
	queens_locations[queen_piece.name] = queen_piece.location

#Calculates board cost
d_attacking_queens = check_diagonal(board_length, queens_locations, d_attacking_queens)
v_attacking_queens = check_vertical(board_length,queens_locations, v_attacking_queens)
h_attacking_queens = check_horizontal(board_length, queens_locations, h_attacking_queens)
current_board_cost = current_board.cost_evaluator(d_attacking_queens, v_attacking_queens, h_attacking_queens)
current_board.set_cost(current_board_cost)
d_attacking_queens.clear()
v_attacking_queens.clear()
h_attacking_queens.clear()

#Displays config list solution
solution_to_display = solution_list(queens_locations)

#Start hill climbing
iterations = 0
while current_board.board_cost != 0:
	queen_solution = steepest_hill_climbing(current_board, queen_piece, queens_locations, d_attacking_queens, v_attacking_queens, h_attacking_queens, board_length)

	queens_locations = queen_solution[0]
	current_board.set_cost(queen_solution[3])
	solution_board_list = queen_solution[2]
	iterations += 1

	#Random restart after 100 iterations of steep hill climbing
	if iterations == 100:
		current_board = Board()
		current_board_list = current_board.create_board(board_length)
		current_board.set_board(current_board_list)
		queens_locations = {}
		d_attacking_queens, v_attacking_queens, h_attacking_queens = [],[],[]

		for col in range(num_of_queens):
			name = 'queen' + str(col + 1)
			queen_piece = Queen(name, board_length)

			#Puts queens in different row randomly
			rand_row = randint(0,board_length - 1)
			current_board_list[rand_row][col] = queen_piece.get_notation()

			#saves queens loc in dict
			queen_piece.location = (col,rand_row)
			queens_locations[queen_piece.name] = queen_piece.location

		d_attacking_queens = check_diagonal(board_length, queens_locations, d_attacking_queens)
		v_attacking_queens = check_vertical(board_length,queens_locations, v_attacking_queens)
		h_attacking_queens = check_horizontal(board_length, queens_locations, h_attacking_queens)
		current_board_cost = current_board.cost_evaluator(d_attacking_queens, v_attacking_queens, h_attacking_queens)
		current_board.set_cost(current_board_cost)
		d_attacking_queens.clear()
		v_attacking_queens.clear()
		h_attacking_queens.clear()
		solution_to_display = solution_list(queens_locations)
		iterations = 0

#Shows final solution with graphic
show_graphic_solution(board_length, solution_board_list, queen_solution[1])