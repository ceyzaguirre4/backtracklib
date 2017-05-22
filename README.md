# BackTrackLib

Easy to use tools for eficient backtracking through recursion.

## Solve

### Overview:

` solve(calculate_posibles_func, basecase, [number_of_answers], [max_time]) `

`calculate_posibles_func` receives a list with earlier choices and must return an iterable with posible choices for the current step.

`basecase` receives a list with earlier choices and returns a boolean value to indicate it has reached a valid answer or not.

`number_of_answers` is an integer which can be passed to indicate the number of answers to be calculated. Default value is 1. If number of answers is set to 0 then all posible answers will be computed.

`max_time ` is an intefer which can be passed to indicate the maximum time the algorithm should run (in seconds). Default value permits it to run undisturbed. Should the time limit be reached, the algorithm will return all answers found up to this point.

` solve ` returns a list with all answers found, the time it took (in seconds), and a boolean value to indicate whether it found all the answers or not (if the time limit was reached). This value will always be True if all possible values were found even if the quantity is lower than `number_of_answers`.


#### Example code: 8 queens
~~~python
from backtracklib import solve

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
	return ret	# list of all posible new positions.

# default values for quantity and time are used: will take as much time as needed to find ONE answer.
answers, time, found_all = solve(calculate_posibles, basecase)
~~~

### Optimizations and heuristics:

All user entered heuristics and optimizations should be implemented in ` calculate_posibles_func `. A general rule of thumb to having a somewhat optimized algorithm is to build ` calculate_posibles_func ` in such a way that `basecase` has to check as little conditions as possible. 

In some problems inputs can be subdivided into discrete sets of elements such that no posible answer will ever have two elements of the same set. In these cases its generally more efficient to only have ` calculate_posibles_func ` return valid elements of one set instead of all valid elements. Future versions of this module will implement this automatically.

If a discretization such as described in the paragraph above is possible then the algorithm can be further optimized by ordering the sets in such a way that ` calculate_posibles_func ` will access first the sets with the most elements. Future versions of this module will also implement this automatically.

Heuristics are dificult to find and generally unique to the problem. Some more general ones will maybe be one day implemented but for now they must be defined by the user and implemented in ` calculate_posibles_func `. Heuristics that asign a higher probability of succes to any element within the set of posibles should be implemented by ordering the return iterable of ` calculate_posibles_func ` by probability (in descending order).