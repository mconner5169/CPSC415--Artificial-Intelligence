'''
CPSC 415 -- Homework #3 project file
Morgan Conner, University of Mary Washington, fall 2021
'''
#import pdb; pdb.set_trace()

import random
import math
from copy import deepcopy
from chess_player import ChessPlayer

class mconner_ChessPlayer(ChessPlayer):
	piece_values = {'p':1,'f':2,'b':3,'n':3,'s':4,'r':5,'q':9,'k':99,
					'P':1,'F':2,'B':3,'N':3,'S':4,'R':5,'Q':9,'K':99}
	
	def __init__(self, board, color):
		super().__init__(board, color)
		self.moves = 0
		self.current_state = None
		self.tree = []
		self.total_board_score = 0
		self.moves_to_score_dict = {}

	def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
			
		#First two moves are random
		while self.moves <= 2:
			self.moves += 1
			mconner_ChessPlayer.piece_evaluator(self,self.board)
			my_move = random.choice(self.board.get_all_available_legal_moves(self.color))
			print("Board score is {}".format(self.total_board_score))
			return my_move

		mconner_ChessPlayer.piece_evaluator(self,self.board)


		#Real stratgy
		h_moves_to_score_dict = self.tree_creator()
		print("tree length is {}\n".format(len(self.tree)))
		
		best_score_with_board = self.minimax()

		#Gets next tuple move
		current_board_state = self.current_state[2]
		print("Best board score only {}\n".format(best_score_with_board))

		#searches dict to add next moves with same score to list
		print("Moves with score {}".format(self.moves_to_score_dict))
		moves_with_same_score = []
		for move, score in self.moves_to_score_dict.items():
			if best_score_with_board == score:
				self.moves_with_same_score.append(move)

		#randomly chooses next move because all scores are the same otherwise choses only score in list
		next_move = random.choice(self.moves_with_same_score)
		print("Next move {}".format(next_move))
		if next_move in self.board.get_all_available_legal_moves(self.color):
			self.tree.clear()
			self.moves_to_score_dict.clear()
			return next_move
		else:
			next_move = list(next_move)
			next_move = (next_move[1], next_move[0])
			self.tree.clear()
			return next_move


	
	def piece_evaluator(self, the_board): #heuristic
		#if score is positive - white is winning; score is negative - black is winning
		for pos,piece in the_board.items():
			if piece.get_notation().isupper():
				self.total_board_score += mconner_ChessPlayer.piece_values[piece.get_notation()]
			else:
				self.total_board_score -= mconner_ChessPlayer.piece_values[piece.get_notation()]
		
	def hypothetical_evaluator(the_board, starting_total_score):
		hypo_score = starting_total_score
		for pos,piece in the_board.items():
			if piece.get_notation().isupper():
				hypo_score += mconner_ChessPlayer.piece_values[piece.get_notation()]
			else:
				hypo_score -= mconner_ChessPlayer.piece_values[piece.get_notation()]

		return hypo_score

	def tree_node(self, board, score, level, name):
		if len(self.tree) == 0:
			#add parent node
			self.tree.append([0, score, board, name])
		else:
			self.tree.append([level, score, board, name])

		return self.tree[-1] #sets current state

	def tree_creator(self): 
		current_depth = 1
		level = current_depth
		board_name = 'A'
		h_moves_to_score_dict = {}
		if self.color == 'white':
			opp_color = 'black'
		else:
			opp_color = 'white'

		curr_board = deepcopy(self.board)

		#added parent node
		self.current_state = self.tree_node(curr_board, self.total_board_score, 0, 'parent') 
		
		my_possible_moves = self.board.get_all_available_legal_moves(self.color)

		#creates first level
		for move in my_possible_moves:
			hypothetical_board = deepcopy(self.board)
			starting_total_score = self.total_board_score
			start = move[0]
			end = move[1]
			
			hypothetical_board.make_move(start,end)
			hypo_score = mconner_ChessPlayer.hypothetical_evaluator(hypothetical_board, starting_total_score)
			self.moves_to_score_dict[(start,end)] = hypo_score #stores tuple move and scored to be referenced later
			self.tree_node(hypothetical_board, hypo_score, level, board_name) #add hypothetical move and data to tree
			board_name = chr(ord(board_name) + 1) #increments to next letter
		

		#creates second level
		h_board_name = 'A'
		for node in self.tree:
			if node[-1] != 'parent': #bypasses parent node
				if node[0] == 1 and node[-1] == h_board_name:
					#print("Node for second level {}".format(node))
					h_board = node[2]
					h_board_possible_moves = h_board.get_all_available_legal_moves(self.color)
					for move in h_board_possible_moves:
						h_hypothetical_board = deepcopy(h_board)
						h_starting_total_score = node[1]
						h_start = move[0]
						h_end = move[1]

						h_hypothetical_board.make_move(h_start,h_end)
						h_hypo_score = mconner_ChessPlayer.hypothetical_evaluator(h_hypothetical_board, h_starting_total_score)
						h_moves_to_score_dict[(h_start, h_end)] = h_hypo_score
						self.tree_node(h_hypothetical_board, h_hypo_score, (level + 1), (h_board_name + h_board_name))

				h_board_name = chr(ord(h_board_name) + 1)
			
		return h_moves_to_score_dict
	
	
	def minimax(self, depth=2):
		scores = []
		leaf_score = 0
		old_child_score = 0
		
		last_board_name = self.tree[-1][-1]
		last_board_letter = last_board_name[0]
		ending_board_letter = chr(ord(last_board_letter) + 1)
		ending_board_name = (ending_board_letter + ending_board_letter)
		print("Last board name {}\n".format(last_board_name))
		start_board_name = 'A'

		#assigns score from leaf node to child
		while board_name != last_board_name:
			for node in self.tree:
				if node[0] == 1 and node[-1] == board_name:
					child_node = node
				if node[0] == 2 and node[-1] == (board_name + board_name):
					scores.append(node[1])

			#sets the child nodes score to the appropriate leaf score
			if self.color == 'white':
				leaf_score = min(scores)
			else:
				leaf_score = max(scores)

			old_child_score = child_node[1]
			child_node[1] = leaf_score

			#updates self.moves_to_score_dict with new score from leaf
			for move, score in self.moves_to_score_dict.items():
				if old_child_score == score:
					child_move = move
			self.moves_to_score_dict[child_move] = leaf_score
			board_name = chr(ord(board_name) + 1)

		#returns child score to root
		scores.clear()
		for child in self.tree:
			if child[0] == 1:
				scores.append(child[1])
		if self.color == 'white':
			root_score = max(scores)
		else:
			root_score = min(scores)

		#print("Update list of level one scores {}".format(scores))
		return root_score
		'''
		for node in self.tree:
			if node[0] == 1:
				depth = 1 #deep_level = 1
			elif node[0] == 2:
				depth = 2 #deep_level = 2
		print("Tree depth is {}\n".format(depth))
		
		minimax_board_name = 'A'
		if depth == 2: #deep_level == 2: 
			for node in self.tree:
				if node[0] == 2 and node[-1] == (minimax_board_name + minimax_board_name):
					scores.append(self.minimax(depth - 1))
				minimax_board_name = chr(ord(minimax_board_name) + 1)	
			
			if self.color == 'white':
				maximum_score = max(scores)
			else:
				maximum_score = min(scores)
			
			return maximum_score

		else: #returning the max value and board from the min nodes
			for child in self.tree:
				if child[0] == 1:
					scores.append(child[1])
					#boards.append(child[2])
				else:
					#append scores
					scores.append(child[1]) 
			if self.color == 'white':
				maximum_score = max(scores)
			else:
				maximum_score = min(scores)
			
			return maximum_score
		'''