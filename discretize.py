import itertools
from threading import Thread

# experimental, algorithm to analize posible separation of posible steps into discrete non-overlaping sets.

def sub(l1, l2, base):
    ret = []
    for elem in l1:
        if elem not in l2 and elem != base:
            ret.append(elem)
    return ret

def incompatibles(x, y, calculate_posibles):    # necesario?
    x = calculate_posibles([x])
    if y not in x: return True
    return False

def fully_incompatible(conjunto, calculate_posibles):
    for elem1 in conjunto:
        for elem2 in conjunto:
            if elem1 != elem2 and not incompatibles(elem1, elem2, calculate_posibles):
                return False
    return True

def max_incompatible(setx, calculate_posibles):
    ret = []
    for i in range(len(setx)):
        subs = list(itertools.combinations(setx, len(setx)-i))
        for sub in subs:
            if fully_incompatible(sub, calculate_posibles):
                ret.append(list(sub))
        if ret:
            return ret
    return False

def full_set(listas, todo):
    total = []
    for lista in listas:
        total += lista
    if set(total) == set(todo):
        return True
    return False

def min_full_set(setx, todo):   # min? 
    ret = []
    for i in range(len(setx)):
        subs = list(itertools.combinations(setx, i))
        for sub in subs:
            if full_set(sub, todo):
                return sub
                ret.append(sub)
        if ret:
            return ret
    return False

def discretize(calculate_posibles):
    ronda1 = calculate_posibles([])
    ronda2 = []
    vistos = []     # cambiar a set

    def function(elem):
        if elem not in vistos:
            incompatibles_x = sub(ronda1, calculate_posibles([elem]) , elem)
            subset_max_incompatibles = max_incompatible(incompatibles_x, calculate_posibles)
            for subset in subset_max_incompatibles:
                ronda2.append([elem] + subset)
                vistos.extend(subset)
                vistos.append(elem)

    for elem in ronda1:
        thread = Thread(target=function, args=(elem,))
        thread.run()
    posibles = min_full_set(ronda2, ronda1)
    return posibles

if __name__ == "__main__":

    def calculate_posibles_queens(parcial):

        # 4 queens problem: position 4 queens on a chessboard so that no one attacks another (simplification of 4s)

        ret = []
        for x in range(4):
            for y in range(4):
                is_in = False
                for i in range(4):
                    if (x,i) in parcial or (i, y) in parcial or (x-i, y-i) in parcial or (x+i, y+i) in parcial:
                        is_in = True
                if not is_in: 
                    ret.append((x,y))
        return ret

    posibles = discretize(calculate_posibles_queens)
    for posible in posibles:
        print(posible)