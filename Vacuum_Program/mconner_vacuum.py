#!/usr/bin/env python3
'''
CPSC 415 -- Homework #1 VacuumAgent file
Morgan Conner
'''

from vacuum import VacuumAgent
import random

class MconnerVacuumAgent(VacuumAgent):

	def __init__(self):
		super().__init__()
		self.moves = 0 #total moves
		self.x = 0 #current x
		self.y = 0 #current y
		self.nx = 0 #next x
		self.ny = 0 #next y
		self.tempx = 0 #temp x
		self.tempy = 0 #temp y
		self.current_action = 'NoOp'
		self.prev_action = 'NoOp'
		self.action_list = list()
		self.visited = set()
		self.visited.add((0,0))
		

	def program(self, percept):
		if self.moves >= 675:
			return 'NoOp'
		if percept[0] == 'Dirty' and percept[1] == 'None':
			self.moves += 1
			return 'Suck'
		if percept[0] == 'Dirty' and percept[1] == 'Bump':
			self.moves += 1
			return 'Suck'
		if percept[0] == 'Clean' and percept[1] == 'None':

			next_action = random.choice(VacuumAgent.possible_actions[:-2:])
			
			#Calculating potential next actions coordinates
			if next_action == 'Right':
				self.tempx = self.x + 1
			elif next_action == 'Left':
				self.tempx = self.x - 1
			elif next_action == 'Up':
				self.tempy = self.y + 1
			elif next_action == 'Down':
				self.tempy = self.y - 1

			self.nxt_coord = (self.tempx, self.tempy)
			
			#If next spot is already visited get new action
			if self.nxt_coord in self.visited:
				UpdatedAction_list = VacuumAgent.possible_actions[:-2:]

				if next_action == 'Right':
					UpdatedAction_list.pop(0)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Up':
						self.ny = self.y + 1
					elif next_action == 'Down':
						self.ny = self.y - 1
				
				elif next_action == 'Left':
					UpdatedAction_list.pop(1)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Up':
						self.ny = self.y + 1
					elif next_action == 'Down':
						self.ny = self.y - 1

				elif next_action == 'Up':
					UpdatedAction_list.pop(2)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Down':
						self.ny = self.y - 1

				elif next_action == 'Down':
					UpdatedAction_list.pop(3)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Up':
						self.ny = self.y + 1
			else:
				#set the potential next action coords to next action coords
				self.nx = self.tempx
				self.ny = self.tempy

			#sets next action coords to current coordinates
			self.x = self.nx
			self.y = self.ny
			self.current = (self.x, self.y)

			#Updates initializations
			self.visited.add(self.current)
			self.action_list.append(next_action)

			self.current_action = self.action_list[-1]
			if len(self.action_list) >=2:
				self.prev_action = self.action_list[-2]

			self.moves += 1
		
			return next_action

		if percept[0] == 'Clean' and percept[1] == 'Bump':

			next_action = random.choice(VacuumAgent.possible_actions[:-2:])
			
			#Ensures next action isn't the same action that caused bump
			while next_action == self.current_action:
				next_action = random.choice(VacuumAgent.possible_actions[:-2:])		

			if next_action == 'Right':
				self.tempx = self.x + 1
			elif next_action == 'Left':
				self.tempx = self.x - 1
			elif next_action == 'Up':
				self.tempy = self.y + 1
			elif next_action == 'Down':
				self.tempy = self.y - 1

			self.nxt_coord = (self.tempx, self.tempy)

			if self.nxt_coord in self.visited:
				UpdatedAction_list = VacuumAgent.possible_actions[:-2:]
				if next_action == 'Right':
					UpdatedAction_list.pop(0)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Up':
						self.ny = self.y + 1
					elif next_action == 'Down':
						self.ny = self.y - 1
				
				elif next_action == 'Left':
					UpdatedAction_list.pop(1)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Up':
						self.ny = self.y + 1
					elif next_action == 'Down':
						self.ny = self.y - 1

				elif next_action == 'Up':
					UpdatedAction_list.pop(2)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Down':
						self.ny = self.y - 1

				elif next_action == 'Down':
					UpdatedAction_list.pop(3)
					next_action = random.choice(UpdatedAction_list)
					if next_action == 'Right':
						self.nx = self.x + 1
					elif next_action == 'Left':
						self.nx = self.x - 1
					elif next_action == 'Up':
						self.ny = self.y + 1
			else:
				self.nx = self.tempx
				self.ny = self.tempy

			self.x = self.nx
			self.y = self.ny
			self.current = (self.x, self.y)
			
			self.visited.add(self.current)
			self.action_list.append(next_action)

			self.current_action = self.action_list[-1]
			if len(self.action_list) >=2:
				self.prev_action = self.action_list[-2]
			
			self.moves += 1
			
			return next_action
			
		return 'NoOp' #