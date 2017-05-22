from time import time

def solve(CalcularPosibles, basecase, num_answers=1, max_time=0):
    parcial = []
    answers = []
    time_start = time()
    try:
        limit = recursive_solve(parcial, answers, num_answers if num_answers != 0 else float('inf'), max_time, time_start,  CalcularPosibles, basecase)
        found_all = False if (limit and len(answers) < num_answers) else True
        return answers, time() - time_start, found_all
    except RecursionError:
        raise Exception("Maximum recursion depth exceeded")
    except Exception as exc:
        raise Exception(exc)

def recursive_solve(parcial, answers, num_answers, max_time, time_start,  CalcularPosibles, basecase):
    def _add(posible):
        parcial.append(posible)
    def _remove():
        parcial.pop()

    if max_time and time() - time_start > max_time:
        return True
    if basecase(parcial):
        answers.append(list(parcial))
        return False if len(answers) < num_answers else True
    else:
        posibles = CalcularPosibles(parcial)
        p = 0
        solved = False
        while not solved and p < len(posibles):
            posible = posibles[p]
            _add(posible)
            solved = recursive_solve(parcial, answers, num_answers, max_time, time_start,  CalcularPosibles, basecase)
            _remove()
            p += 1
        return solved
