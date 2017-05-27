from time import time

def a(calc_posibles, start, basecase, heuristic=None, time_limit=10, reverse=False):
	time_limit = float('inf') if time_limit == 0 else time_limit
	start_time = time()
	stack = _Stack(start, heuristic)
	while time() < start_time + time_limit:
		if not stack: return False
		cur_position = stack.pop()
		if basecase(cur_position.value): return stack._full_path(cur_position, reverse)
		alrededor = calc_posibles(cur_position.value)
		for elem, cost in alrededor:
			stack._binary_insert(elem, heuristic, cur_position, cost)
	raise TimeoutError("Time limit reached, you can manually change or remove it.")

class _Node:
	def __init__(self, value, heuristic_func, father=None, path_cost=1):
		self.value = value
		self.heuristic_cost = 0 if not heuristic_func else heuristic_func(self.value)
		self.accumulated_cost = father.accumulated_cost + path_cost if father else 0
		self.father = father

	def __eq__(self, other):
		if self.value == other:
			return True
		return False

	def __repr__(self):
		return str(self.value)

class _Stack(list):
	def __init__(self, start, heuristic):
		super().__init__()
		self.append(_Node(start, heuristic))

	def _binary_insert(self, value, heuristic, father, cost):	# adds new elements and updates values for elements that already where included.
		# orders from higher to lower, to reverse change (1), (2) for their indicated comparison
		def _added_cost(elem):
			return elem.heuristic_cost + elem.accumulated_cost

		if len(self):
			accumulated_cost = cost + father.accumulated_cost
			added_cost = accumulated_cost if not heuristic else heuristic(value) + accumulated_cost
			begining, end = 0, len(self)
			split = (begining + end)//2
			while end - begining > 1:
				if added_cost >= _added_cost(self[split]):			# (1) <
					end = split
				else:
					begining = split
				split = (begining + end)//2
			found = self[begining:end][0]
			if value == found.value:
				if accumulated_cost < found.accumulated_cost:
					found.accumulated_cost = accumulated_cost
					found.father = father
			elif added_cost > _added_cost(self[begining:end][0]):		# (2) <
				self[begining:begining] = [_Node(value, heuristic, father, cost)]
			else:
				self[end:end] = [_Node(value, heuristic, father, cost)]
		else:
			self.append(_Node(value, heuristic, father, cost))


	def _full_path(self, position, reverse):
		if reverse: return self._gen_full_path(position)
		return list(self._gen_full_path(position))[::-1]

	def _gen_full_path(self, position):	# tiene mas sentido si parto por el ultimo.
		while position != None:
			yield position.value
			position = position.father