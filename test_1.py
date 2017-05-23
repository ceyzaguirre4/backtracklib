from backtracklib import Solver

# 8 queens problem: position 8 queens on a chessboard so that no one attacks another.

def basecase(parcial):
	if len(parcial) == 4:
		return True
	return False

def calculate_posibles(parcial):
	ret = []
	for x in range(4):
		for y in range(4):
			is_in = False
			for i in range(4):
				if (x,i) in parcial or (i, y) in parcial or (x-i, y-i) in parcial or (x+i, y+i) in parcial:
					is_in = True
			if not is_in: 
				ret.append((x,y))
	return ret

gen = Solver(calculate_posibles, basecase)
# answer has not been searched for
answer1 = gen.solutions[0]	# answer is computed
print(gen.tree)

def test_1():
	assert basecase(answer1)

if __name__ == "__main__":
	print(answer1)