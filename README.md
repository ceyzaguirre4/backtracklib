# BackTrackLib

Easy to use tools for eficient backtracking through recursion.

## Resolver

` resolver(calculate_posibles_func, basecase, [number_of_answers], [max_time]) `

`calculate_posibles_func` receives a list with earlier choices and must return an iterable with posible choices for the current step.

`basecase` receives a list with earlier choices and returns a boolean value to indicate it has reached a valid answer or not.

`number_of_answers` is an integer which can be passed to indicate the number of answers to be calculated. Default value is 1. If number of answers is set to 0 then all posible answers will be computed.

`max_time ` is an intefer which can be passed to indicate the maximum time the algorithm should run (in seconds). Default value permits it to run undisturbed. Should the time limit be reached, the algorithm will return all answers found up to this point.

` resolver ` returns a list with all answers found, the time it took (in seconds), and a boolean value to indicate whether it found all the answers or not (if the time limit was reached). This value will always be True if all possible values were found even if the quantity is lower than `number_of_answers`.


#### Example code: 8 queens
~~~python
from backtracklib import resolver

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

answers, time, found_all = resolver(calculate_posibles, basecase)
~~~