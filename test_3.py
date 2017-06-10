from non_recursive_backtracking import NonSolver

# 8 queens problem: position 8 queens on a chessboard so that no one attacks another.

def basecase(parcial):
	if len(parcial) == 8:
		return True
	return False

def calculate_posibles(parcial):
	ret = []
	for x in range(8):
		for y in range(8):
			is_in = False
			for i in range(8):
				if (x,i) in parcial or (i, y) in parcial or (x-i, y-i) in parcial or (x+i, y+i) in parcial:
					is_in = True
			if not is_in: 
				ret.append((x,y))
	return ret

# uses a non recursive algorithm to backtrack

gen = NonSolver(calculate_posibles, basecase)
answer = gen.solutions

def test_1():
	assert basecase(next(answer))

if __name__ == "__main__":
	print(next(answer))