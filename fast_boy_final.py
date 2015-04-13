#uses the MCTS with full rollout 
# reward function should be the current players score minus the 
# other players score

from node import Node 
from math import *
import time
import random

THINK_DURATION = 1

def think(state, quip):

    t_start = time.time()
    t_deadline = t_start + THINK_DURATION

    iterations = 0
    time_limit_reached = False

    rootnode = Node(state = state)   
    def outcome(score):
        if node.who == 'red':
            return score['red'] - score['blue']
        else:
            return score['blue'] - score['red']



    # iteration max, once time is more than one second end while
    # if it has not finished on  its own already 

    while True:
        iterations += 1
        
        node = rootnode
        rollout_state = state.copy()


        # select 
        while not rollout_state.is_terminal() and node.children != []:
            node = node.select_child()
            rollout_state.apply_move(node.move)

        # Expand
        if not rollout_state.is_terminal(): # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untried_moves) 
            rollout_state.apply_move(m)
            node = node.add_child(m,rollout_state) # add child and descend tree
        terminate = 0
        while not (rollout_state.is_terminal()) and terminate < 5: # while state is non-terminal
            if rollout_state.is_terminal():
                    break
            rollout_move = random.choice(rollout_state.get_moves())
            rollout_state.apply_move(rollout_move)
            terminate += 1


        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.update(outcome(rollout_state.get_score())) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parent
        
        t_now = time.time()
        if t_now > t_deadline:
            time_limit_reached = True
            break
            
        # if its been more than a second then the it exits from the loop    


    sample_rate = float(iterations)/(t_now - t_start)
    print "iterations per second is : ", sample_rate 

    # return the move that was most visited
    return sorted(rootnode.children, key = lambda c: c.visits)[-1].move 

	
