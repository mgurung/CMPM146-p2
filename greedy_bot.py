# greety_bot.py

# chooses a legal move that maximizes the immediate score gain
# looks 1 move into the future and chooses the one that increases its 
# score the most
import random

MAX_DEPTH = 1

# chooses a legal move randomly
def think(state, quip):
	
	moves = state.get_moves()
	
	best_move = moves[0]
	highest_score = 0;

	for move in moves:

		total_score = 0.0

		greedy_state = state.copy()
		greedy_state.apply_move(move)

		for i in range(MAX_DEPTH):

			if greedy_state.is_terminal():
				break
			greety_move = random.choice(greedy_state.get_moves())
			greedy_state.apply_move(greety_move)

		total_score = greedy_state.get_score()

		if total_score > highest_score:
			highest_score = total_score
			best_move = move


	return best_move

