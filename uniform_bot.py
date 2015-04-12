# uniform_bot.py
# choose amongst legal moves uniformly 
import random

# chooses a legal move randomly
def think(state, quip):
	uniform_move  = random.choice(state.get_moves())
	return uniform_move

