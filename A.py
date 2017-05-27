from time import time

_all_nodes = {}

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
		_all_nodes[self.value] = self

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
	
	def _update(self, other, other_cost, other_father, heuristic):	# adds new elements and updates values for elements that already where included.
		if other in _all_nodes:
			node = _all_nodes[other]
			other_cost = other_cost + other_father.accumulated_cost
			if other_cost < node.accumulated_cost:
				node.accumulated_cost = other_cost
				node.father = other_father
			return
		self._binary_insert(_Node(other, heuristic, other_father, other_cost))

	def _binary_insert(self, elem):		# orders from higher to lower added_cost, reverse: change (1), (2) for their indicated comparison
		def _added_cost(elem):
			return elem.heuristic_cost + elem.accumulated_cost

		if len(self):
			added_cost = _added_cost(elem)
			begining, end = 0, len(self)
			split = (begining + end)//2
			while end - begining > 1:
				if added_cost >= _added_cost(self[split]):			# (1) <
					end = split
				else:
					begining = split
				split = (begining + end)//2
			if added_cost > _added_cost(self[begining:end][0]):		# (2) <
				self[begining:begining] = [elem]
			else:
				self[end:end] = [elem]
		else:
			self.append(elem)


	def _full_path(self, position, reverse):
		_all_nodes.clear()
		if reverse: return self._gen_full_path(position)
		return list(self._gen_full_path(position))[::-1]

	def _gen_full_path(self, position):	# tiene mas sentido si parto por el ultimo.
		while position != None:
			yield position.value
			position = position.father