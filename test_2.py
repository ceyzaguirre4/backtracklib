from backtracklib import solve

# 8 queens problem: position 8 queens on a chessboard so that no one attacks another.

def basecase(parcial):
	if len(parcial) == 8:
		return True

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

answers, time, found_all = solve(calculate_posibles, basecase)

def test_1():
	assert basecase(answers[0])

if __name__ == "__main__":
	test_1()
	print(answers)