class NonSolver:
	def __init__(self, calculate_posibles, basecase):
		self.calculate_posibles = calculate_posibles
		self.basecase = basecase
		self.solutions = self._solve()

	def _solve(self):
		partial = []
		calcs = [self.calculate_posibles(partial)]
		depth = 0
		while True:
			if self.basecase(partial):
				yield partial.copy()
			if depth == len(calcs):
				calcs.append(self.calculate_posibles(partial))
			posibles = calcs[depth]
			if posibles:
				partial.append(posibles.pop())
				depth += 1
			else:
				if not depth:
					break
				depth -= 1
				partial.pop()
				calcs.pop()


if __name__ == "__main__":
	n_queens = 8

	def basecase(partial):
		if len(partial) == n_queens:
			return True
		return False

	def calculate_posibles(partial):
		ret = []
		for x in range(n_queens):
			for y in range(n_queens):
				is_in = False
				for i in range(n_queens):
					if (x,i) in partial or (i, y) in partial or (x-i, y-i) in partial or (x+i, y+i) in partial:
						is_in = True
				if not is_in: 
					ret.append((x,y))
		return ret
	gen = NonSolver(calculate_posibles, basecase)
	print(next(gen.solutions))
