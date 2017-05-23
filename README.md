# BackTrackLib

Easy to use tools for eficient backtracking through recursion.

## Solver

### Overview:

` Solver(<calculate_posibles_func>, <basecase_func>) `

Solver class is designed to compute and represent answers to all backtracking problems. It receives two user defined functions at initialization:

`calculate_posibles_func` receives a list with earlier choices and must return an iterable with posible choices for the current step.

`basecase_func` receives a list with earlier choices and returns a boolean value to indicate it has reached a valid answer or not.

### Using `Solver` to find answers:

Answers are not computed when the object is created. If no solutions have been computed yet, upon accesing `.solutions` of a object of class `Solver` one solution will be computed and returned automatically. Alternatively the `.solve` method can be used.

#### Atributes:
` .solutions ` is a list with all answers found, `.time` is the time it took (in seconds) to compute, and ` found_all` is a boolean value to indicate whether it found all the answers requested or not. This value will always be True if all possible values were found even if the quantity is lower than `number_of_answers`, so ` found_all` will only be false if the time limit was reached.

More granular control over the amount of solutions or the maximum time the search should take can be had by using the `.solve` method.

`<solver_object>.solve([number_of_answers=1], [max_time=0])`

`number_of_answers` is an integer which can be passed to indicate the number of answers to be calculated. Default value is 1. If number of answers is set to 0 then all posible answers will be computed.

`max_time ` is an integer which can be passed to indicate the maximum time the algorithm should run (in seconds). Default value (0) permits it to run undisturbed. Should the time limit be reached, the algorithm will return all answers found up to this point.

#### Example code: 8 queens

~~~python
from backtracklib import Solver

# 8 queens problem: position 8 queens on a chessboard so that no one attacks another.

def basecase(parcial):
	if len(parcial) == 8:
		return True
	return False

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

gen = Solver(calculate_posibles, basecase)
# answer has not been searched for yet.
answer1 = gen.solutions[0]		# answer is computed.
~~~

### Solution Trees:

Solver class objects also include a `.tree` atribute which represents the recursion tree. This atribute can be printed using the python built-in method `print(<solver_object>.tree)`.

#### Example output

~~~
(0, 0)>	(1, 2)>	(2, 1)
		(3, 1)
	(1, 3)>	(2, 1)
		(3, 1)
		(3, 2)
	(2, 1)>	(1, 2)
		(1, 3)
	(2, 3)>	(3, 1)
		(3, 2)
	(3, 1)>	(1, 2)
		(1, 3)
		(2, 3)
	(3, 2)>	(1, 3)
		(2, 3)
(0, 1)>	(1, 0)>	(2, 2)
		(3, 3)
	(1, 3)>	(2, 0)>	(3, 2)
~~~


### Optimizations and heuristics:

All user entered heuristics and optimizations should be implemented in ` calculate_posibles_func `. A general rule of thumb to having a somewhat optimized algorithm is to build ` calculate_posibles_func ` in such a way that `basecase` has to check as little conditions as possible. 

In some problems inputs can be subdivided into discrete sets of elements such that no posible answer will ever have two elements of the same set (ie. in the above example no two queens will ever be in the same column). In these cases its generally more efficient to only have ` calculate_posibles_func ` return valid elements of one set instead of all valid elements. Future versions of this module will implement this automatically.

If a discretization such as described in the paragraph above is possible then the algorithm can be further optimized by ordering the sets in such a way that ` calculate_posibles_func ` will access first the sets with the most elements. Future versions of this module will also implement this automatically.

Heuristics are dificult to find and generally unique to the problem. Some more general ones will maybe be one day implemented but for now they must be defined by the user and implemented in ` calculate_posibles_func `. Heuristics that asign a higher probability of succes to any element within the set of posibles should be implemented by ordering the return iterable of ` calculate_posibles_func ` by probability (in descending order).