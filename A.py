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
			stack._update(elem, cost, cur_position, heuristic)
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

class _Stack(list):
	def __init__(self, start, heuristic):
		super().__init__()
		self.append(_Node(start, heuristic))
	
	def _update(self, other, other_cost, other_father, heuristic):	# adds new elements and updates values for elements that already where included.
		for node in self:
			if node.value == other:
				other_cost = other_cost + other_father.accumulated_cost
				if other_cost > node.accumulated_cost:
					node.path_cost = other_cost
					node.father = other_father
				return
		self.append(_Node(other, heuristic, other_father, other_cost))		# change to use that list is ordered
		self.sort(key=lambda x: x.heuristic_cost + x.accumulated_cost, reverse=True)


	def _full_path(self, position, reverse):
		if reverse: return self._gen_full_path(position)
		return list(self._gen_full_path(position))[::-1]

	def _gen_full_path(self, position):	# tiene mas sentido si parto por el ultimo.
		while position != None:
			yield position.value
			position = position.father
