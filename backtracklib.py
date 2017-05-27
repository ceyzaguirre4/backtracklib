from time import time
from threading import Thread

class _rec_tree:
    def __init__(self, value=None, base=None, depth=0):
        self.base = base
        self.value = value
        self.children = []
        self.depth = depth

    def add_branch(self, value):
        new_tree = _rec_tree(value=value, base=self, depth=self.depth + 1)
        self.children.append(new_tree)
        return new_tree

    def __repr__(self):
        if self.value != None:
            if self.children:
                ret = "{}>\t".format(self.value)
            else:
                ret = "{}".format(self.value)
        else:
            ret = ""
        for n, child in enumerate(self.children):
            if n != 0:
                ret += "\t"*(self.depth)*1
            if n != len(self.children) - 1:
                ret += str(child) + "\n"
            else:
                ret += str(child)
        return ret

class Solver:
    def __init__(self, CalcularPosibles, basecase):
        self.CalcularPosibles = CalcularPosibles
        self.basecase = basecase
        self._tree = _rec_tree()
        self.current_node = self._tree
        self._solutions, self._time, self._found_all = None, None, None

    @property
    def solutions(self):
        if not self._time:
            self.solve()
        return self._solutions

    @property
    def time(self):
        if not self._time:
            self.solve()
        return self._time

    @property
    def found_all(self):
        if not self._time:
            self.solve()
        return self._found_all

    @property
    def tree(self):
        if not self._time:
            self.solve()
        return self._tree

    def solve(self, num_answers=1, max_time=0, threading=False):
        parcial = []
        answers = []
        time_start = time()
        if not threading: 
            limit = self._recursive_solve(parcial, answers, num_answers if num_answers != 0 else float('inf'), max_time, time_start)
        else:
            limit = self._threaded_recursive_solve(parcial, answers, num_answers if num_answers != 0 else float('inf'), max_time, time_start)
        found_all = False if (limit and len(answers) < num_answers) else True
        self._solutions, self._time, self._found_all =  answers, time() - time_start, found_all
        return self._solutions

    def _threaded_recursive_solve(self, parcial, answers, num_answers, max_time, time_start):
        for elem in self.CalcularPosibles(parcial):
            thread = Thread(target=self._recursive_solve, args=(parcial, answers, num_answers, max_time, time_start, True))
            thread.start()

    def _recursive_solve(self, parcial, answers, num_answers, max_time, time_start, threaded=False):
        def _add(posible):
            parcial.append(posible)
            self.current_node = self.current_node.add_branch(posible)
        def _remove():
            parcial.pop()
            self.current_node = self.current_node.base

        if max_time and time() - time_start > max_time:
            return True
        if self.basecase(parcial):
            answers.append(list(parcial))
            return False if len(answers) < num_answers else True
        elif threaded and len(answers) >= num_answers:
            return True
        else:
            posibles = self.CalcularPosibles(parcial)
            p = 0
            solved = False
            while not solved and p < len(posibles):
                posible = posibles[p]
                _add(posible)
                solved = self._recursive_solve(parcial, answers, num_answers, max_time, time_start)
                _remove()
                p += 1
            return solved
