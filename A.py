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
			stack._add_new(elem, cost, cur_position, heuristic)
	raise TimeoutError("Time limit reached, you can manually change or remove it.")

class _Node:
	_all_nodes = {}

	def __init__(self, value, heuristic_func, father=None, path_cost=1):
		self.value = value
		self.heuristic_cost = 0 if not heuristic_func else heuristic_func(self.value)
		self.accumulated_cost = father.accumulated_cost + path_cost if father else 0
		self.father = father
		_Node._all_nodes[self.value] = self

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
	
	def _add_new(self, other, other_cost, other_father, heuristic):	 # inserts new elements and updates values for elements that already where included.
		if other in _Node._all_nodes:
			node = _Node._all_nodes[other]
			other_cost = other_cost + other_father.accumulated_cost
			if other_cost < node.accumulated_cost:
				node.accumulated_cost = other_cost
				node.father = other_father
				self._binary_update(node)	# log( N )
				# self.sort(key= lambda x: x.heuristic_cost + x.accumulated_cost, reverse=True)	# N log( N )
				# assert self == sorted(self, key= lambda x: x.heuristic_cost + x.accumulated_cost, reverse=True)
			return
		self._binary_insert(_Node(other, heuristic, other_father, other_cost))	# log( N )
		# assert self == sorted(self, key= lambda x: x.heuristic_cost + x.accumulated_cost, reverse=True)

	def _binary_insert(self, elem):		# inserts from higher to lower added_cost in log( N ), (reverse: change (1), (2) for their indicated comparison)
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
			if added_cost > _added_cost(self[begining]):			# (2) <
				self[begining:begining] = [elem]
			else:
				self[end:end] = [elem]
		else:
			self.append(elem)

	def _binary_update(self, elem):		# if the added cost was changed then one element can be out of order, this re-sorts in log( N )
		if len(self):
			begining, end = 0, len(self)
			split = (begining + end)//2
			while end - begining > 1:
				if elem.value >= self[split].value:
					end = split
				else:
					begining = split
				split = (begining + end)//2
			if elem.value == self[begining].value:
				del self[begining]
				self._binary_insert(elem)

	def _full_path(self, position, reverse):
		_Node._all_nodes.clear()
		if reverse: return self._gen_full_path(position)
		return list(self._gen_full_path(position))[::-1]

	def _gen_full_path(self, position):
		while position != None:
			yield position.value
			position = position.father
