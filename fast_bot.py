from math import *
import random
import time

ROLLOUTS = 10
MAX_DEPTH = 5

def think(state, quip):

	moves = state.get_moves()

	best_move = moves[0]
	best_expecation = float('-inf')

	me = state.get_whos_turn()

	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']

	for move in moves:

		total_score = 0.0

		for r in range(ROLLOUTS):

			rollout_state = state.copy()

			rollout_state.apply_move(move)


			for i in range(MAX_DEPTH):
				if rollout_state.is_terminal():
					break
				rollout_move = random.choice( rollout_state.get_moves() )
				rollout_state.apply_move( rollout_move )

			total_score += outcome(rollout_state.get_score())

		expectation = float(total_score)/ROLLOUTS

		if expectation > best_expecation:
			best_expecation = expectation
			best_move = move

	print "Picking %s with expected score %f" % (str(best_move), best_expecation)
	return best_move

class Node(object):
	def __init__(self, state, parent=None):
		self.parent = parent
		self.who = state.get_whos_turn()
		self.children = []
		self.untried_moves = state.get_moves()
		self.visits = 0
		self.score = 0.0

	def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.children, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
		
	def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.children.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1

def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)
	rollouts = 0

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        while node.untriedMoves == [] and node.children != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.apply_move(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))
			rollouts++

		print rollouts
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    return sorted(rootnode.children, key = lambda c: c.visits)[-1].move # return the move that was most visited
    