from backtracklib import Solver

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

gen = Solver(calculate_posibles, basecase)
# answer has not been searched for
# answer1 = gen.solutions[0]	# answer is computed
gen.solve(num_answers=1, threading=True)
answers = gen.solutions

# def test_1():
# 	assert basecase(answer1)
# 	assert len(answers) == 1

if __name__ == "__main__":
	print(answers)
	print(len(answers))
