class NonSolver:
	def __init__(self, CalcularPosibles, basecase):
		self.CalcularPosibles = CalcularPosibles
		self.basecase = basecase
		self._solutions, self._time, self._found_all = [], None, None
		self._parcial = []

	@property
	def solutions(self):
		return self._solve()

	def _solve(self):
		calcs = [self.CalcularPosibles(self._parcial)]
		depth = 0
		while True:
			if self.basecase(self._parcial):
				copia = self._parcial.copy()
				self._solutions.append(copia)
				yield copia
			if depth == len(calcs):
				calcs.append(self.CalcularPosibles(self._parcial))
			elif depth > len(calcs):
				raise Exception("depth mayor que el largo")
			posibles = calcs[depth]
			if posibles:
				self._parcial.append(posibles.pop())
				depth += 1
			else:
				if not depth:
					break
				depth -= 1
				self._parcial.pop()
				calcs.pop()
		return self._parcial

n_queens = 4

if __name__ == "__main__":
	def basecase(parcial):
		if len(parcial) == n_queens:
			return True
		return False

	def calculate_posibles(parcial):
		ret = []
		for x in range(n_queens):
			for y in range(n_queens):
				is_in = False
				for i in range(n_queens):
					if (x,i) in parcial or (i, y) in parcial or (x-i, y-i) in parcial or (x+i, y+i) in parcial:
						is_in = True
				if not is_in: 
					ret.append((x,y))
		return ret
	gen = NonSolver(calculate_posibles, basecase)
	print(next(gen.solutions))
