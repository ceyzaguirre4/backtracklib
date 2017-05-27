from A import a

# labrynth is represented by a graph of valid moves.
labrynth = [(0,0), (1,0), (1,1), (1,2), (2,0), (3, 0), (3, 1), (4, 1), (4, 2), (4, 3), (3, 3), (3, 4), (3,5), (3, 2)]
start = (0, 0)
end = (3, 2)

#############################
# Posible heuristics:
#############################

def pythagorean_distance(position):		# heuristic n1
	return (abs(position[0]-start[0])**2 + abs(position[1]-start[1])**2)**0.5

def manhattan_distance(position):		# heuristic n2
	return abs(position[0]-start[0]) + abs(position[1]-start[1])

#############################
# Calculate posibles (identical for both directions because labrynth is a undirected graph)
#############################

def calculate_posibles(position):		# returns valid moves for a given position
	ret = []
	for valid_move in labrynth: 
		if (valid_move[0] == position[0] and valid_move[1] == position[1] + 1) or (valid_move[0] == position[0] and valid_move[1] == position[1] - 1) or (valid_move[0] == position[0] + 1 and valid_move[1] == position[1]) or (valid_move[0] == position[0] - 1 and valid_move[1] == position[1]): 
			ret.append((valid_move, 1)) 	# tuple contains element and movement cost
	return ret

#############################
# Starting from begining:
#############################

def basecase1(position):	# basecase starting from the begining
	if position == end:
		return True
	return False

answer2 = a(calculate_posibles, start, basecase1)												# from begining to end, returns list

#############################
# Starting from the end:
#############################

def basecase2(position):		# basecase starting from the end
	if position == start:
		return True
	return False

answer1 = a(calculate_posibles, end, basecase2, heuristic=manhattan_distance, reverse=True)		# from back to front, returns generator




def test_1():
 	assert list(answer1) == answer2

if __name__ == "__main__":
	print(list(answer1))
	print(answer2)
