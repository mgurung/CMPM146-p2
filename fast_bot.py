from math import *
import random
import time

MAX_DEPTH = 5
THINKTIME = 1

def think(state, quip):
	rootnode = Node(state = state)
	moves = state.get_moves()

	best_move = moves[0]
	best_expecation = float('-inf')
	
	t_start = time.time()
	t_deadline = t_start + THINKTIME
	iterations = 0

	me = state.get_whos_turn()

	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']
	
	for move in moves:

		total_score = 0.0
		iterations += THINKTIME

		
		node = rootnode
		rollout_state = state.copy()
		
		for i in range(MAX_DEPTH):
				if rollout_state.is_terminal():
					break
				rollout_move = random.choice( rollout_state.get_moves() )
				rollout_state.apply_move( rollout_move )

				# Select
				while node.untried_moves == [] and node.children != []: # node is fully expanded and non-terminal
					node = node.UCTSelectChild(rollout_state)
					rollout_state.apply_move(node.move)

				# Expand
				if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
					m = random.choice(node.untried_moves) 
					rollout_state.apply_move(m)
					node = node.AddChild(m,rollout_state) # add child and descend tree

				# Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
				while rollout_state.get_moves() != []: # while state is non-terminal
					rollout_state.apply_move(random.choice(rollout_state.get_moves()))

				# Backpropagate
				while node != None: # backpropagate from the expanded node and work back to the root node
					node.Update(outcome(rollout_state.get_score())) # state is terminal. Update node with result from POV of node.playerJustMoved
					node = node.parent
			
		t_now = time.time()
		#print "times are", t_now, t_start
		#sample_rate = float(iterations)/(t_now - t_start)
		if t_now > t_deadline:
			break

	#sample_rate = float(iterations)/(t_now - t_start)		
	
	return sorted(rootnode.children, key = lambda c: c.visits)[-1].move # return the move that was most visited

		
	
	
	print "Picking %s with expected score %f" % (str(best_move), best_expecation)
	return best_move

def reward(state):
		scores = state.get_score()
		me = state.get_whos_turn()
		if me == 'red' and me == max(['red','blue'],key=scores.get):
			return scores[max(['red','blue'],key=scores.get)] - scores[min(['red','blue'],key=scores.get)]
		else:
			return scores[max(['red','blue'],key=scores.get)] - scores[min(['red','blue'],key=scores.get)]
			
			

class Node(object):
	def __init__(self, move = None, state = None, parent=None):
		self.move = move
		self.parent = parent
		self.who = state.get_whos_turn()
		self.children = []
		self.untried_moves = state.get_moves()
		self.visits = 0
		self.score = 0.0

	def UCTSelectChild(self, state):
		""" Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
			lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
			exploration versus exploitation.
		"""
		s = sorted(self.children, key = lambda c: reward(state) + sqrt(2*log(self.visits)/c.visits))[-1]
		return s
		
	def AddChild(self, m, s):
		""" Remove m from untriedMoves and add a new child node for this move.
			Return the added child node
		"""
		n = Node(move = m, parent = self, state = s)
		self.untried_moves.remove(m)
		self.children.append(n)
		return n
    
	def Update(self, result):
		""" Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
		"""
		self.visits += 1
		self.score += result
		