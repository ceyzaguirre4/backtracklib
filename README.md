# BackTrackLib

Easy to use tools for eficient backtracking through recursion.

## Backtracking with Solver class

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

`<solver_object>.solve([number_of_answers=1], [max_time=0], [threading=False])`

`number_of_answers` is an integer which can be passed to indicate the number of answers to be calculated. Default value is 1. If number of answers is set to 0 then all posible answers will be computed.

`max_time ` is an integer which can be passed to indicate the maximum time the algorithm should run (in seconds). Default value (0) permits it to run undisturbed. Should the time limit be reached, the algorithm will return all answers found up to this point.

`threading ` is a boolean value that indicates whether threads should be implemented in the first step or not. The threads will cease function once the number of answers computed is equal to the number asked by the user, but if two threads reach diferent answers at roughly the same time more answers than requested can be returned.

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
answer1 = gen.solutions[0]		# implicit solving
~~~

#### Example code: Knapsack Problem

![MacDown logo](https://imgs.xkcd.com/comics/np_complete.png)

Source: [xkcd](https://xkcd.com/287/)

~~~python
from backtracklib import Solver

def total(parcial):
	total = 0
	for elem in parcial:
		total += elem.price
	return total

def basecase(parcial):
	if total(parcial) == "1505":
		return True
	return False

def calculate_posibles(parcial):
	posibles = []
	for elem in apetizers:	# apetizers should be a list of objects that have a price atribute
		if total(parcial) + elem.price <= 1505:
			posibles.append(elem)
	return posibles
			

gen = Solver(calculate_posibles, basecase)
gen.solve(num_answers=4, threading=True) 	# explicit solving
answers = gen.solutions
~~~

### Solution Trees:

Solver class objects also include a `.tree` atribute which represents the recursion tree. This atribute can be printed using the python built-in method `print(<solver_object>.tree)`.

#### Example output of 4 queens (simplified version of 8 queens)

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

In some problems inputs can be subdivided into discrete sets of elements such that no posible answer will ever have two elements of the same set (ie. in the above example no two queens will ever be in the same column). In these cases its generally more efficient to only have ` calculate_posibles_func ` return valid elements of one set instead of all valid elements.

If a discretization such as described in the paragraph above is possible then the algorithm can be further optimized by ordering the sets in such a way that ` calculate_posibles_func ` will access first the sets with the most elements.

Heuristics are dificult to find and generally unique to the problem. Some more general ones will maybe be one day implemented but for now they must be defined by the user and implemented in ` calculate_posibles_func `. Heuristics that asign a higher probability of succes to any element within the set of posibles should be implemented by ordering the return iterable of ` calculate_posibles_func ` by probability (in descending order).

## A*/Djskra Pathfinding

### Overview:

`path = a(<calculate_posibles_func>, <start>, <basecase>, [heuristic=None], [time_limit=0], [reverse=False]) `

This function is designed to solve all pathfinding problems regardless of whether the map/graph/etc fits in memory or not. In order to achieve this *"one size fits all"* solution control over the heuristics, posible moves for any given position and start point are delegated to the user and integrated into the algorithm. They are passed into the funtion as parameters.

The bare minimums for a path to be found are:

`calculate_posibles_func`: Must return a list of tuples `(next_move, move_cost)` where  `move_cost` must be of type int or float, but `next_move` can be of any type. In order to find all valid  `next_move`'s the function must receive a parameter of the same type as  `next_move` representing the current position of the algorithm.

`start `: must be of identical type as  `next_move`. It indicates the starting point of the algorithm, not necesarily the starting point of the map (for example, it is more eficient to find the way from the end to the start but more on that later).

`basecase `: must be a function that only return `True` when the path arives at its intended destination. For example, in a maze solving problem starting at the entrance,  `basecase` should only return `True` when the current position is the exit of the maze. The function must receive the current position (of whatever type the user decided to create his moves).

The `a()` function returns a list with all the necesary next steps (where the steps are again of the same type as `next_move`) in order to reach the basecase.

More granular control can be had by passing into `a()`:

`heuristic `: is a function that returns a integer or float that represents the likelyhood of a step being the correct one where a lower value means that the step is more likely to be correct than another with a higher `heuristic` return value. It must receive one parameter to indicate the position who's value is to be computed. The one diference between Djskra and A* is the inclusion of this function.

`time_limit`: a integer or float that indicates for how long the algorithm should run. Its default value is `0` which permits it to run indefinetely.

`reverse`: a booean that tells the algorithm whether or not it is computing the steps from *"back to front"* (end to begining, instead of the more traditional begining to end). Setting this value to `True` speeds up the extraction of the answer in `a()` by returning a generator object instead of a list. This is generally better if the length of the answer doesnt fit in its allocated memory or if the user doesnt need to know the full path all at once, but rather just the first n-steps that bring it closer to the endpoint (for example, in a game where the path will be re-computed every few miliseconds to consider terrain changes). If set to `True` both `start` and `basecase` have to change to reflect the new direction, and sometimes also `calculate_posibles_func ` also has to change (eg: if the map is a directed graph (some directions are only permited one-way), or the `move_cost ` is diferent (uphill vs downhill)).

#### Example code: Maze solving

~~~python
from A import a

# labrynth is represented by a graph of valid moves.
labrynth = [(0,0), (1,0), (1,1), (1,2), (2,0), (3, 0), (3, 1), (4, 1), (4, 2), (4, 3), (3, 3), (3, 4), (3,5), (3, 2)]
start = (0, 0)
end = (3, 2)

#############################
# Some posible heuristics:
#############################

def pythagorean_distance(position):		# heuristic n1
	return (abs(position[0]-start[0])**2 + abs(position[1]-start[1])**2)**0.5

def manhattan_distance(position):		# heuristic n2
	return abs(position[0]-start[0]) + abs(position[1]-start[1])

#############################
# Calculate posibles (identical for both directions because labrynth is a undirected graph and move_cost is always 1)
#############################

def calculate_posibles(position):		# returns valid moves for a given position
	ret = []
	for valid_move in labrynth: 
		if (valid_move[0] == position[0] and valid_move[1] == position[1] + 1) or (valid_move[0] == position[0] and valid_move[1] == position[1] - 1) or (valid_move[0] == position[0] + 1 and valid_move[1] == position[1]) or (valid_move[0] == position[0] - 1 and valid_move[1] == position[1]): 
			ret.append((valid_move, 1)) 	# tuple contains element and movement cost
	return ret

#############################
# Starting from begining:
#############################

def basecase1(position):	# basecase starting from the begining
	if position == end:
		return True
	return False

answer1 = a(calculate_posibles, start, basecase1)  # from begining to end, returns list (no heuristic:Djskra; no time limit)

#############################
# Starting from the end:
#############################

def basecase2(position):		# basecase starting from the end
	if position == start:
		return True
	return False

answer2 = a(calculate_posibles, end, basecase2, heuristic=manhattan_distance, reverse=True)  # from back to front, returns generator (includes heuristic cost function: A*)
~~~
